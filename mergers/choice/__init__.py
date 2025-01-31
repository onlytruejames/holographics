from components import VariableManager
from random import random

class Merger:
    name = "choice"
    description = "Chooses randomly between the two frames"
    variables = {
        "Preference": VariableManager("Preference", float, 0.5, "Float ranging from 0-1 denoting preference for the new image over the previous image")
    }
    def merge(self, img1, img2):
        if random() < self.variables["Preference"].value:
            return img2
        return img1