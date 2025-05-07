from PIL import Image
import numpy as np
from components import VariableManager

class Module:
    name = "palette"
    description = "Changes the colour palette of an image"
    variables = {
        "Colours": VariableManager(
            "Colours",
            "list",
            [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0)
            ],
            "Changes the colour palette of the image"
        ),
        "Rate": VariableManager("Rate", "integer", 1, "Amount the offset increments by each frame")
    }
    palettes = {}
    val = 0
    def message(self, id, message):
        match id:
            case "variableUpdate":
                if message == "Colours":
                    palette = [tuple(p) for p in self.variables["Colours"].value]
                    key = str(palette)
                    if not key in self.palettes:
                        p_img = Image.new('P', (16, 16))
                        lenPaletteSector = int(256 / len(palette))
                        newPal = [item for sublist in palette for item in sublist * lenPaletteSector]
                        for i in range(int((768 - len(newPal)) / 3)):
                            newPal.append(palette[0][0])
                            newPal.append(palette[0][1])
                            newPal.append(palette[0][2])
                        p_img.putpalette(newPal)
                        self.palettes[key] = p_img
                    self.p_img = self.palettes[key]
        
    def requestFrame(self, img):
        img = np.array(img.convert("L"), dtype="int64") + self.val
        img = Image.fromarray(np.mod(img, 255).astype("uint8"))
        self.val += self.variables["Rate"].value
        return img.quantize(palette=self.p_img).convert("RGBA")