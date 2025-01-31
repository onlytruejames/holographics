from PIL import Image
import numpy as np
from components import VariableManager
import math as maths

class Module:
    def __init__(self):
        self.name = "expandingColours"
        self.description = "Dissolve effect which works by setting the value of a pixel to the brightest, nearest value in its surroundings from the current or previous frame."
        self.variables = {
            "Radius": VariableManager("Radius", "int", 2, "Radius over which the dissolve effect operates for any pixel. Controls number of pixels."),
            "Decay": VariableManager("Decay", "float", 0.2, "Amount the brightness of the previous image is reduced by"),
            "Spread": VariableManager("Spread", "int", 1, "Distance multiplier for the pixels in radius. Does not affect the number of pixels, only how far apart they are.")
        }
        self.dimensions = (100, 100)
        self.previousImage = np.array(Image.new("RGBA", self.dimensions, (0, 0, 0, 255)))
        self.coords = []
        self.subtraction = self.variables["Decay"].value * 255

    def message(self, id, data):
        match id:
            case "dimensions":
                self.dimensions = data
                prevImg = Image.fromarray(self.previousImage.astype(np.uint8))
                self.previousImage = np.array(prevImg.resize(data, Image.NEAREST)).astype(np.float32)
            case "variableUpdate":
                if data == "Radius" or data == "Spread":
                    # Reset list of offsets
                    spread = self.variables["Spread"].value
                    r = self.variables["Radius"].value * spread
                    rsquared = r**2
                    self.coords = [(x * spread, y * spread) for x in range(-r, r+1, 1) for y in range(-r, r+1, 1) if (x**2 + y**2) <= rsquared]
                elif data == "Decay":
                    self.subtraction = self.variables["Decay"].value * 255
    
    def requestFrame(self, image):
        sum = np.array(image).astype(np.float32)
        prevSum = self.previousImage - self.subtraction
        sums = [np.roll(prevSum, coord, (0, 1)) for coord in self.coords]
        sums.append(sum)
        sum = np.maximum.reduce(sums)
        self.previousImage = sum
        return Image.fromarray(sum.astype(np.uint8))