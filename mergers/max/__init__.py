from PIL import Image
import numpy as np
class Merger:
    def __init__(self):
        self.name = "max"
        self.description = "Replace the maximum RGBA values from each pixel"
    def merge(self, img1, img2):
        return Image.fromarray(
            np.maximum(
                np.array(img1),
                np.array(img2)
            )
        )