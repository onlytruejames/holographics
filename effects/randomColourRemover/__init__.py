from PIL import Image, ImageFilter
import numpy as np
import random
from components import VariableManager

gaussian = ImageFilter.GaussianBlur()

class Module:
    def __init__(self):
        self.name = "randomColourRemover"
        self.description = "Removes a random colour from the image"
        self.variables = {
            "Preserve Colour": VariableManager("Preserve Colour", "boolean", True, "Preserve only the random colour or remove only the random colour?")
        }

    def requestFrame(self, img):
        originalMask = np.array(img.getchannel("A"))
        # Get colour coordinates
        coords = (random.randint(0, img.width - 1), random.randint(0, img.height - 1))
        # Blur image slightly
        mask = np.array(img.filter(gaussian).convert("L")).astype("int64")
        # Subtract colour
        mask -= mask[coords[1], coords[0]]
        # Create mask with 0 and 1
        mask = np.clip(np.floor(np.abs(mask)) - 10, 0, 1)
        if self.variables["Preserve Colour"].value:
            mask = 1 - mask
        # Apply mask with 0 and 255 instead
        mask = mask.astype(np.uint8) * 255
        mask = np.minimum(mask, originalMask)
        img.putalpha(Image.fromarray(mask))
        return img