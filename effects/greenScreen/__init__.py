from PIL import Image
import numpy as np
from components import VariableManager

class Module:
    def __init__(self):
        self.name = "greenScreen"
        self.description = "Remove all colours similar to a specified colour."
        self.variables = {
            "Colour": VariableManager("Colour", "RGB", (0, 0, 0), "The colour to be removed"),
            "Proximity": VariableManager("Proximity", "int", 10, "How close does a colour need to be to this colour?")
        }
    
    def requestFrame(self, img):
        originalMask = np.array(img.getchannel("A"))
        mask = np.array(img.convert("RGB")).astype(np.int64)
        # Subtract colour
        mask = np.abs(mask - np.array(self.variables["Colour"].value))
        mask = np.sum(mask, 2)
        mask = np.where(mask < self.variables["Proximity"].value, 0, 255)
        mask = np.minimum(mask, originalMask)
        img.putalpha(Image.fromarray(mask.astype(np.uint8)))
        return img