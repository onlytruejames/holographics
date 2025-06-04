from components import VariableManager
from PIL import Image, ImageSequence
from random import choice
from os import walk, path

cache = {}

class Module:
    def __init__(self):
        self.name = "mediaLoader"
        self.description = "Returns image files"
        self.imageInfo = {
            "imageWidth": 10,
            "imageHeight": 10,
            "frames": []
        }
        self.dimensions = (100, 100) # default
        #self.imageInfo["imageWidth"] = 10
        #self.imageInfo["imageHeight"] = 10
        #self.imageInfo["frames"] = []
        self.blankImage = None # Assigned in the message method
        self.index = 0
        # Assign variables as an attribute so it is externally available
        self.variables = {
            "Preserve Aspect Ratio": VariableManager("Preserve Aspect Ratio", "boolean", True, "When resizing the camera photo, preserve the aspect ratio?"),
            "Media Location": VariableManager("Media Location", "string", "", "Location of the media's file"),
            "Random Sequence": VariableManager("Random Sequence", "boolean", False, "If animated, display the frames in a random order?"),
            "Cache": VariableManager("Cache", "boolean", True, "Cache this media file for future use?"),
            "Is Cache Module": VariableManager("CacheModule", "boolean", False, "Is this module only being used to cache an image?")
        }
        # Below are relevant variables to zoomToFit
        self.resizeDims = None # Dimensions the media is resized to
        self.resizeCoordinate = [0, 0] # And the coordinate it is pasted onto

    def animated(self, image):
        # The image parameter is not used
        # If the media is animated, send it to the next frame and process this
        self.imageInfo["frames"].append(self.imageInfo["frames"].pop(0))
        return self.imageInfo["frames"][-1]
    
    def randimated(self, image):
        # Return random frame
        return choice(self.imageInfo["frames"])
    
    def static(self, image):
        return self.imageInfo["frames"][0]

    def message(self, id, data):
        match id: # Decide what to do with the message based on its identifier
            case "dimensions":
                self.dimensions = data
                self.blankImage = Image.new("RGBA", self.dimensions, (0, 0, 0, 0))
                # First we compare the aspect ratios of the media file and the 
                # requested dimensions. Aspect ratio is width / height, which can be 
                # interpreted as the wideness of an image.
                medAspectRatio = self.imageInfo["imageWidth"] / self.imageInfo["imageHeight"]
                dimAspectRatio = self.dimensions[0] / self.dimensions[1]
                if medAspectRatio > dimAspectRatio:
                    # Media is wider than the dimensions, proportionally.
                    width = self.dimensions[0] # The camera image will be the width of the dimensions.
                    # Media width / Dimensions width = Media height / Dimensions  height. So output height = Media height * (Dimensions width /  Media width)
                    height = self.imageInfo["imageHeight"] * (self.dimensions[0] / self.imageInfo["imageWidth"])
                else:
                    # The opposite of the previous part
                    height = self.dimensions[1]
                    width = self.imageInfo["imageWidth"] * (self.dimensions[1] / self.imageInfo["imageHeight"])
                self.resizeDims = (int(width), int(height))
                coordinate = (
                    (self.blankImage.width - self.resizeDims[0]) // 2,
                    (self.blankImage.height - self.resizeDims[1]) // 2
                ) # Halfway between (0, 0) and the difference between the dimensions 
                # results in a centred placement. Also rounded to be an integer.
                self.resizeCoordinate = coordinate
                self.loadFrames()
            case "variableUpdate":
            	if data == "Media Location":
                    self.loadFrames()
            case _:
                pass
    
    def frameProcess(self, image):
        image = image.convert("RGBA")
        preservesAR = self.variables["Preserve Aspect Ratio"].value # Is the aspect ratio being preserved?
        if not preservesAR:
            return image.resize(self.dimensions)
        else:
            image = image.resize(self.resizeDims)
            # Assuming that the method for pasting an image on top of another image 
            # (place(lower, upper, coordinate)) places the top left corner of the upper
            # image at the specified coordinate on the lower image
            blank = self.blankImage.copy()
            blank.paste(image, self.resizeCoordinate)
            return blank
    
    def requestFrame(self, image):
        return image # This function gets changed immediately OR the module is only being used to cache an image

    def loadFrames(self):
        location = self.variables["Media Location"].value
        if not location in cache:
            try:
                image = Image.open(location)
                self.imageInfo["imageWidth"] = image.width
                self.imageInfo["imageHeight"] = image.height # Update values of dimensions
                self.imageInfo["frames"] = ImageSequence.all_frames(image, self.frameProcess) # Get list of frames
            except:
                fnames = []
                for (dirpath, dirnames, names) in walk(location):
                    fnames.extend(names)
                    break
                frames = []
                for f in fnames:
                    try:
                        frames.append(self.frameProcess(Image.open(path.join(location, f))))
                    except:
                        pass
                self.imageInfo["imageWidth"], self.imageInfo["imageHeight"] = frames[0].width, frames[0].height
                self.imageInfo["frames"] = frames
            if self.variables["Cache"].value:
                cache[location] = self.imageInfo
        else:
            self.imageInfo = cache[location]
        if len(self.imageInfo["frames"]) == 1:
            self.requestFrame = self.static
        elif self.variables["Random Sequence"].value:
            self.requestFrame = self.randimated
        else:
            self.requestFrame = self.animated
        if self.variables["Is Cache module"].value:
            self.requestFrame = self.requestFrame
        self.index = 0 # Reset frame index