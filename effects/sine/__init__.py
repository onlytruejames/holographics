from components import VariableManager
import numpy as np
from PIL import Image

class Module:
    def __init__(self):
        self.name = "sine"
        self.description = "Returns the sine of a frame"
        self.variables = {
            "Multiplier": VariableManager("Multiplier", "float", 1, "How much are the RGB values multiplied by before performing sine?")
        }
    
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = np.array(image).astype(np.float64)
        image *= (self.variables["Multiplier"].value)
        image = (image + 1) * 127.5
        image = Image.fromarray(image.astype(np.uint8))
        image.putalpha(alpha)
        return image