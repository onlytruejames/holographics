from components import VariableManager
from PIL import Image
import numpy as np

class Merger:
    def __init__(self):
        self.name = "diffCompare"
        self.description = "Compares the change in brightness across an image between the newly-processed frame and either the previous frame or the unprocessed frame"
        self.variables = {
            "Compare": VariableManager("Compare", "string", "Unprocessed", "(Unprocessed/Previous) Determines which frame to compare with"),
            "Mode": VariableManager("Mode", "string", "Max", "(Max/Min) Determines whether to compare which image has lower/higher pixel differences")
        }

    def getDifferences(self, img):
        img = img.astype(np.int8)
        img = np.abs(img - np.roll(img, 1))
        return img

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
        img1Diff = self.getDifferences(img1)
        img2Diff = self.getDifferences(img2)
        if self.variables["Mode"].value == "Max":
            image = np.where(img1Diff > img2Diff, img1, img2)
        else:
            image = np.where(img1Diff < img2Diff, img1, img2)
        image = Image.fromarray(image)
        self.lastImg = image
        return image