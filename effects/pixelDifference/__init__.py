from PIL import Image
import numpy as np
from components import EffectVariable

class Module:
    def __init__(self):
        self.name = "pixelDifference"
        self.description = "Return the difference a pixel has to its neighbouring pixels"
        self.variables = {
            "Mode": EffectVariable("Mode", "string", "maximum", "Find the maximum/minimum/average difference from the surround pixels, or find the difference from 1 pixel left/right/up/down.")
        }
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = np.array(image).astype(np.int16)
        match self.variables["Mode"].value:
            case "up":
                img2 = np.roll(image, -1, 0)
                image = np.abs(image - img2)
            case "down":
                img2 = np.roll(image, 1, 0)
                image = np.abs(image - img2)
            case "left":
                img2 = np.roll(image, -1, 1)
                image = np.abs(image - img2)
            case "right":
                img2 = np.roll(image, 1, 1)
                image = np.abs(image - img2)
            case "maximum":
                image = np.maximum.reduce([
                    np.abs(image - np.roll(image, -1, 0)),
                    np.abs(image - np.roll(image, 1, 0)),
                    np.abs(image - np.roll(image, -1, 1)),
                    np.abs(image - np.roll(image, 1, 1))
                ])
            case "minimum":
                image = np.minimum.reduce([
                    np.abs(image - np.roll(image, -1, 0)),
                    np.abs(image - np.roll(image, 1, 0)),
                    np.abs(image - np.roll(image, -1, 1)),
                    np.abs(image - np.roll(image, 1, 1))
                ])
            case "average":
                image = (
                    np.abs(image - np.roll(image, -1, 0)) +
                    np.abs(image - np.roll(image, 1, 0)) +
                    np.abs(image - np.roll(image, -1, 1)) +
                    np.abs(image - np.roll(image, 1, 1))
                ) // 4
        image = Image.fromarray(image.astype(np.uint8))
        image.putalpha(alpha)
        return image