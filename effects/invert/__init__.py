from PIL import ImageChops
from components import EffectVariable

class Module:
    def __init__(self):
        self.name = "invert"
        self.description = "Inverts an image"
        self.variables = {
            "Preserve Transparency": EffectVariable("Preserve Transparency", "boolean", True, "Preserve the transparency of the original image")
        }
    
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = ImageChops.invert(image)
        image.putalpha(alpha)
        return image