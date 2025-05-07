from PIL import Image
import numpy as np
from components import VariableManager
from random import choice, randint

class Module:
    def __init__(self):
        self.name = "stretch"
        self.description = "Copy a line of pixels to the edge perpendicular to it"
        self.variables = {
            "Area": VariableManager("Area", "float", 1, "(0-1) The proportion of the length/height of the image along which rows are selectable"),
            "Rate": VariableManager("Rate", "int", 0, "The mean number of frames between changes to which row is copied")
        }
        self.dims = [100, 100]
        self.newLine()
    
    def newLine(self):
        self.mode = choice(["x", "y"])
        if self.mode == "x":
            length = self.dims[1]
        else:
            length = self.dims[0]
        self.line = randint(0, self.variables["Area"].value * length / 2)
        self.negative = choice([True, False])
    
    def message(self, id, data):
        match id:
            case "dimensions":
                self.dims = data
            case "variableUpdate":
                self.newLine()
    
    def requestFrame(self, img):
        try:
            image = np.array(img)
            if self.mode == "x":
                if self.negative:
                    slice = np.array([image[-self.line] for i in range(self.line)])
                    image[-self.line-1:-1] = slice
                else:
                    slice = np.array([image[self.line] for i in range(self.line)])
                    image[0:self.line] = slice
            else:
                if self.negative:
                    slice = [image[:, -self.line] for i in range(self.line)]
                    slice = np.swapaxes(slice, 0, 1)
                    image[:, -self.line-1:-1] = slice
                else:
                    slice = [image[:, self.line] for i in range(self.line)]
                    slice = np.swapaxes(slice, 0, 1)
                    image[:, 0:self.line] = slice
            if randint(0, self.variables["Rate"].value) == 0:
                self.newLine()
            return Image.fromarray(image)
        except:
            return img