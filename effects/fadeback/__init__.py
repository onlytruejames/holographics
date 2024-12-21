from PIL import Image
import numpy as np
from components import EffectVariable

class Module:
    def __init__(self):
        self.name = "fadeback"
        self.description = "Create a 3D-style effect by pasting the previous frame behind this one, but slightly smaller."
        self.variables = {
            "Rate": EffectVariable("Rate", "integer", 1, "Number of pixels the image shrinks by each frame"),
            "Mode": EffectVariable("Mode", "integer", 0, "(0-5): Specifies the resizing mode from [NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS]"),
            "Reducing Gap": EffectVariable("Reducing Gap", "integer", 1, "Specify the reducing gap of the resizing function.")
        }
        self.modes = [
            Image.NEAREST,
            Image.BOX,
            Image.BILINEAR,
            Image.HAMMING,
            Image.BICUBIC,
            Image.LANCZOS
        ]
        self.mode = Image.NEAREST
        self.lastImg = Image.new("RGBA", (100, 100))
        self.blank = self.lastImg.copy
        self.dims = (100, 100)
    
    def message(self, id, data):
        match id:
            case "dimensions":
                self.lastImg = self.lastImg.resize(data)
                self.blank = Image.new("RGBA", data)
                amount = self.variables["Rate"].value * 2
                self.dims = (
                    data[0] - amount,
                    data[1] - amount
                )
        
    def requestFrame(self, image):
        amount = self.variables["Rate"].value
        last = self.lastImg.resize(self.dims, self.modes[self.variables["Mode"].value], reducing_gap=self.variables["Reducing Gap"].value)
        blank = self.blank.copy()
        blank.alpha_composite(last, (amount, amount))
        blank.alpha_composite(image)
        self.lastImg = blank
        return blank