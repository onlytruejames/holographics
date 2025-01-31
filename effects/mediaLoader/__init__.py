from components import VariableManager
from PIL import Image, ImageSequence
class Module:
    def __init__(self):
        self.name = "mediaLoader"
        self.description = "Returns image files"
        self.dimensions = (100, 100) # default
        self.imageWidth = 10
        self.imageHeight = 10
        self.index = 0
        self.frames = []
        self.blankImage = None # Assigned in the message method
        preserveAR = VariableManager("Preserve Aspect Ratio", "boolean", True, "When resizing the camera photo, preserve the aspect ratio?")
        mediaLocation = VariableManager("Media Location", "string", "", "Location of the media's file")
        # Assign variables as an attribute so it is externally available
        self.variables = {"Preserve Aspect Ratio": preserveAR, "Media Location": mediaLocation}
        # Below are relevant variables to zoomToFit
        self.resizeDims = None # Dimensions the media is resized to
        self.resizeCoordinate = [0, 0] # And the coordinate it is pasted onto

    def animated(self, image):
        # The image parameter is not used
        # If the media is animated, send it to the next frame and process this
        self.frames.append(self.frames.pop(0))
        return self.frames[-1]
    
    def static(self, image):
        return self.frames

    def message(self, id, data):
        match id: # Decide what to do with the message based on its identifier
            case "dimensions":
                self.dimensions = data
                self.blankImage = Image.new("RGBA", self.dimensions, (0, 0, 0, 0))
                # First we compare the aspect ratios of the media file and the 
                # requested dimensions. Aspect ratio is width / height, which can be 
                # interpreted as the wideness of an image.
                medAspectRatio = self.imageWidth / self.imageHeight
                dimAspectRatio = self.dimensions[0] / self.dimensions[1]
                if medAspectRatio > dimAspectRatio:
                    # Media is wider than the dimensions, proportionally.
                    width = self.dimensions[0] # The camera image will be the width of the dimensions.
                    # Media width / Dimensions width = Media height / Dimensions  height. So output height = Media height * (Dimensions width /  Media width)
                    height = self.imageHeight * (self.dimensions[0] / self.imageWidth)
                else:
                    # The opposite of the previous part
                    height = self.dimensions[1]
                    width = self.imageWidth * (self.dimensions[1] / self.imageHeight)
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
        return image # Gets changed immediately

    def loadFrames(self):
        image = Image.open(self.variables["Media Location"].value)
        self.imageWidth = image.width
        self.imageHeight = image.height # Update values of dimensions
        self.frames = ImageSequence.all_frames(image, self.frameProcess) # Get list of frames
        if len(self.frames) == 1:
            self.frames = self.frames[0]
            self.requestFrame = self.static
        else:
            self.requestFrame = self.animated
        self.index = 0 # Reset frame index