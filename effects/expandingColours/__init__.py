from PIL import Image
import numpy as np
from components import EffectVariable
import math as maths

class Module:
    def __init__(self):
        self.name = "expandingColours"
        self.description = "Dissolve effect which works by setting the value of a pixel to the brightest, nearest value in its surroundings from the current or previous frame."
        radius = EffectVariable("Radius", "int", 2, "Radius over which the dissolve effect operates for any pixel")
        decay = EffectVariable("Decay", "float", 0.8, "Multiplier of pixel brightness of the previous frame")
        self.variables = {
            "Radius": radius,
            "Decay": decay
        }
        self.dimensions = (100, 100)
        self.previousImage = np.array(Image.new("RGBA", self.dimensions, (0, 0, 0, 255)))
        self.coords = [(0, 0)]
        self.subtraction = self.variables["Decay"].value * 255

    def message(self, id, data):
        match id:
            case "dimensions":
                self.dimensions = data
                prevImg = Image.fromarray(self.previousImage.astype(np.uint8))
                self.previousImage = np.array(prevImg.resize(data)).astype(np.float32)
            case "variableUpdate":
                if data == "Radius":
                    # Reset list of offsets
                    r = self.variables["Radius"].value
                    rsquared = r**2
                    self.coords = [(x, y) for x in range(-r, r+1, 1) for y in range(-r, r+1, 1) if (x**2 + y**2) <= rsquared]
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