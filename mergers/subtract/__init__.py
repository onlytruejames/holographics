from PIL import Image
import numpy as np
from components import VariableManager

class Merger:
    name = "subtract"
    description = "Subtracts the new image from the previous image"
    variables = {
        "Reverse Order": VariableManager("Reverse Order", "boolean", False, "Default order is the previous frame subtracted from the new frame. Reverse this order?")
    }
    def merge(self, img1, img2):
        if self.variables["Reverse Order"].value:
            temp = img1
            img1 = img2
            img2 = temp
            del temp
        alpha = img1.getchannel("A")
        img = np.array(img1).astype(np.int16)
        img2 = np.array(img2).astype(np.int16)
        img -= img2
        img = np.clip(img, 0, 255)
        img = Image.fromarray(img.astype(np.uint8))
        img.putalpha(alpha)
        return img