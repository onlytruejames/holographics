from PIL import Image
import numpy as np
from components import VariableManager

class Merger:
    name = "inverseChange"
    description = "Inverts all RGB changes"
    variables = {
        "Compare": VariableManager("Compare", "string", "Unprocessed", "(Unprocessed/Previous) Determines which frame to compare with")
    }
    lastImg = False
    
    def merge(self, old, new):
        alpha = new.getchannel("A")
        if self.variables["Compare"].value == "Previous":
            try:
                assert self.lastImg.size == new.size
                old = self.lastImg.copy()
            except:
                pass
            self.lastImg = new.copy()
        old = np.array(old, np.int16)
        new = np.array(new, np.int16)
        img = Image.fromarray(np.clip((2 * old) - new, 0, 255).astype(np.uint8))
        img.putalpha(alpha)
        return img