from PIL.Image import alpha_composite
class Merger:
    def __init__(self):
        pass
    def merge(self, img1, img2):
        return alpha_composite(img2, img1)