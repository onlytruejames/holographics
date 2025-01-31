from uuid import uuid4
from importlib import import_module
from os import listdir

def importEffectModules():
    directories = listdir("effects") # List all directories in holographics/effects
    classes = {} # Create a dictionary to contain the names and Module classes of all the effect modules
    for dir in directories:
        try:
            importedModule = import_module(f"effects.{dir}").Module # Import the module class from the effect module
            classes[dir] = importedModule # Assign this module to the dictionary of classes
        except Exception as e:
            print(f"Error caught in importEffectModules: {e}")
            # Non-importable directory, do nothing
            pass
    return classes

EffectClasses = importEffectModules()

def importMergerModules():
    directories = listdir("mergers") # List all directories in holographics/mergers
    classes = {} # Create a dictionary to contain the names and Merger classes of all the merger modules
    for dir in directories:
        try:
            importedModule = import_module(f"mergers.{dir}").Merger # Import the merger class from the merger module
            classes[dir] = importedModule # Assign this module to the dictionary of classes
        except Exception as e:
            print(f"Error caught in importMergerModules: {e}")
            # Non-importable directory, do nothing
            pass
    return classes

MergerClasses = importMergerModules()

def createMerger(data: dict):
    merger = MergerClasses[data["mergerName"]]() # Instantiated merger instance
    try:
        assert merger.variables
    except:
        return merger
    if not "mergerVariables" in data:
        data["mergerVariables"] = {}
    for var in data["mergerVariables"]:
        if var in merger.variables:
            merger.variables[var].value = data["mergerVariables"][var]
    return merger

class Slide:
    def __init__(self):
        # Add random Id of slide for future use, and blank effects list
        self.slideId = uuid4()
        self.effects = []
    def load(self, effects):
        effectsList = [] # Empty list of effects to be assigned to this.effects
        for eff in effects:
            if not "merger" in eff:
                eff["merger"] = {"mergerName": "replace"}
            if not "effectVariables" in eff:
                eff["effectVariables"] = {}
            newEffect = Effect(eff["effectName"], eff["merger"], eff["effectVariables"])
            # Create effect object of given type with correct composite mode and variables
            effectsList.append(newEffect) # Add to list of effects
        self.effects = effectsList

class Effect:
    def __init__(self, moduleName, merger, variables=None):
        # HOW THE INHERITANCE WORKS:
        # All attributes of this class can be defined here.
        # self.effectId, self.merger
        # Static attributes of Module can be inherited here.
        # self.name, self.description
        # Methods and dynamic attributes of Module need getters, setters, and wrappers so 
        # their scopes remain in the Module class so are available outside new().
        # self.requestFrame, self.message, self.variables
        # There will be a dictionary called Classes which contains the names and Module objects of all modules
        self.module = EffectClasses[moduleName]() # Create new instance of the correct Module
        self.effectId = uuid4() # As with earlier, not implementing this
        self.merger = createMerger(merger)
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