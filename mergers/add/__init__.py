from PIL import Image
import numpy as np

class Merger:
    def __init__(self):
        self.name = "add"
        self.description = "Adds the RGBA values of the pixels together"
    def merge(self, img1, img2):
        img1 = np.array(img1).astype(np.uint16) + np.array(img2).astype(np.uint16)
        img1 = np.clip(img1, 0, 255)
        return Image.fromarray(img1.astype(np.uint8))