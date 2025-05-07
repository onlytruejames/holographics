from PIL import Image, ImageFilter
import numpy as np
from components import VariableManager

gauss1 = ImageFilter.GaussianBlur(radius=4)
gauss2 = ImageFilter.GaussianBlur(radius=8)

class Module:
    name = "dogDiff"
    description = "Returns the difference between pixels across the image as determined by Difference Of Gaussians"
    variables = {
        "Mode": VariableManager("Mode", "string", "Apply", "(Apply/Raw) Whether to return the image weighted by difference (Apply) or return only the difference (Raw)")
    }
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = image.convert("RGB")
        img3 = np.abs(np.array(image.filter(gauss1), dtype="int64") - np.array(image.filter(gauss2), dtype="int64"))
        if self.variables["Mode"].value == "Raw":
            out = Image.fromarray(img3.astype(np.uint8))
            out.putalpha(alpha)
            return out
        alpha = np.array(alpha).astype(np.float64) * np.sum(img3, 2) / 255
        alpha = Image.fromarray(alpha.astype(np.uint8))
        image.putalpha(alpha)
        return image