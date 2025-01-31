from PIL import Image
import numpy as np

class Merger:
    def __init__(self):
        self.name = "multiply"
        self.description = "Multiplies images together. Multiplication results from 0-255^2 are mapped to 0-255 when it comes to RGBA values."
    def merge(self, img1, img2):
        img1 = np.array(img1).astype(np.int16)
        img2 = np.array(img2).astype(np.int16)
        img1 = (img1 * img2) // 256
        return Image.fromarray(img1.astype(np.uint8))