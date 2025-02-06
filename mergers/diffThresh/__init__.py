from components import VariableManager
from PIL import Image
import numpy as np

class Merger:
    def __init__(self):
        self.name = "diffCompare"
        self.description = "Compares the change in brightness across an image between the newly-processed frame and either the previous frame or the unprocessed frame"
        self.variables = {
            "Compare": VariableManager("Compare", "string", "Unprocessed", "(Unprocessed/Previous) Determines which frame to compare with"),
            "Threshold": VariableManager("Threshold", "integer", 50, "Amount a pixel needs to change for it to appear on the image")
        }

    def merge(self, img1, img2):
        try:
            assert self.lastImg
        except Exception as e:
            self.lastImg = img1
            return img1
        if self.variables["Compare"].value == "Unprocessed":
            img2 = np.array(img2)
        else:
            img2 = np.array(self.lastImg)
        img1 = np.array(img1)
        imgDiff = np.abs(img1.astype(np.int8) - img2.astype(np.int8))
        image = np.where(imgDiff > self.variables["Threshold"].value, img1, img2)
        image = Image.fromarray(image.astype(np.uint8))
        self.lastImg = image
        return image