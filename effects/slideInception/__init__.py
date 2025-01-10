# A slide within a slide
from PIL import Image
from components import EffectVariable
from uuid import uuid4
from importlib import import_module
from os import listdir

def importModules():
    directories = listdir("effects") # List all directories in holographics/effects
    classes = {} # Create a dictionary to contain the names and Module classes of all the effect modules
    for dir in directories:
        try:
            if dir == "slideInception":
                continue
            importedModule = import_module(f"effects.{dir}").Module # Import the module class from the effect module
            classes[dir] = importedModule # Assign this module to the dictionary of classes
        except Exception as e:
            print(f"Error caught in importModules: {e}")
            # Non-importable directory, do nothing
            pass
    classes["slideInception"] = Module
    return classes

class Slide:
    def __init__(self):
        # Add random Id of slide for future use, and blank effects list
        self.slideId = uuid4()
        self.effects = []
    def load(self, effects):
        effectsList = [] # Empty list of effects to be assigned to this.effects
        for eff in effects:
            if not "compositeMode" in eff:
                eff["compositeMode"] = "replace"
            if not "effectVariables" in eff:
                eff["effectVariables"] = {}
            newEffect = Effect(eff["effectName"], eff["compositeMode"], eff["effectVariables"])
            # Create effect object of given type with correct composite mode and variables
            effectsList.append(newEffect) # Add to list of effects
        self.effects = effectsList

class Effect:
    def __init__(self, moduleName, compositeMode="replace", variables=None):
        # HOW THE INHERITANCE WORKS:
        # All attributes of this class can be defined here.
        # self.effectId, self.compositeMode
        # Static attributes of Module can be inherited here.
        # self.name, self.description
        # Methods and dynamic attributes of Module need getters, setters, and wrappers so 
        # their scopes remain in the Module class so are available outside new().
        # self.requestFrame, self.message, self.variables
        # There will be a dictionary called Classes which contains the names and Module objects of all modules
        self.module = Classes[moduleName]() # Create new instance of the correct Module
        self.effectId = uuid4() # As with earlier, not implementing this
        self.compositeMode = compositeMode
        self.name = self.module.name
        for var in variables:
            self.module.variables[var].value = variables[var] # Variables from text to objects
            self.message("variableUpdate", var)
        # Test for module description, if not present leave blank
        try:
            self.description = self.module.description
        except:
            self.description = ""

    def requestFrame(self, image):
        try:
            return self.module.requestFrame(image)
        except Exception as e:
            print(f"Error in {self.name}.requestFrame")
            raise e

    def message(self, id, data):
        # Send a message if possible, but if the method is written badly, just print the id and data of the message.
        try:
            self.module.message(id, data)
        except Exception as e:
            print(f"Error caught in {self.name}.message: {e}")
            print(f"Message ID: {id}, Message Payload: {data}")
    
    @property
    def variables(self):
        '''Wrapper for self.module.variables'''
        return self.module.variables

    @variables.setter
    def variables(self, value):
        try:
            assert self.module.variables # Will cause an exception if not present
            prevVariables = self.module.variables # Used to figure out what changed
            self.module.variables = value
            # Tell the module which variables have changed
            for var in value:
                if not prevVariables[var] == value[var]:
                    self.message("variableUpdate", var)
        except Exception as e:
            print(f"Error caught in {self.name}.variables.setter: {e}")
            pass # Do nothing

class Module:
    def __init__(self):
        self.name = "effectInception"
        self.description = "Create another independent slide and return the results"
        self.variables = {
            "Slide": EffectVariable("Slide", "slide", [], "Slide data for the independent slide")
        }
        self.dimensions = (100, 100)
        self.blankImage = Image.new("RGBA", self.dimensions, (0, 0, 0, 0)) # Create an empty transparent image to apply the first effect to
        self.blackImage = Image.new("RGBA", self.dimensions, (0, 0, 0, 255)) # Create a black image to paste the image onto at the end
        self.currentSlide = Slide()

    def message(self, id, data):
        match id:
            case "dimensions":
                for eff in self.currentSlide.effects:
                    eff.message("dimensions", data)
                self.blankImage = Image.new("RGBA", data, (0, 0, 0, 0)) # Create an empty transparent image to apply the first effect to
                self.blackImage = Image.new("RGBA", data, (0, 0, 0, 255)) # Create a black image to paste the image onto at the end
            case "variableUpdate":
                self.slide = self.createSlide()

    def requestFrame(self, image):
        image = self.blankImage.copy()
        for eff in self.currentSlide.effects: # Iterate through all effects and process frames through all
            newImage = eff.requestFrame(image).copy()
            # Decide how to composite the new and old frames together
            match eff.compositeMode:
                # At first I'm only supporting "front", "behind", and "replace".
                case "front":
                    image = Image.alpha_composite(image, newImage)
                case "behind":
                    image = Image.alpha_composite(newImage, image)
                case "replace":
                    image = newImage
        return image

    def createSlide(self):
        newSlide = Slide() # Create slide
        newSlide.load(self.variables["Slide"].value) # Load into slide
        for eff in newSlide.effects:
            eff.message("dimensions", self.dimensions) # Message to inform effects of dimensions
        self.currentSlide = newSlide

Classes = importModules()