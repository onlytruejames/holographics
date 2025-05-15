from PIL import Image
import numpy as np

class Module:
    name = "colourNormalise"
    description = "Turns brightness up to maximum everywhere, but preserves the relative RGB values"
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        r = np.array(image.getchannel("R")).astype(np.float64)
        g = np.array(image.getchannel("G")).astype(np.float64)
        b = np.array(image.getchannel("B")).astype(np.float64)
        brightness = (r + g + b) / 765
        r = np.clip(r // brightness, 0, 255)
        g = np.clip(g // brightness, 0, 255)
        b = np.clip(b // brightness, 0, 255)
        image = Image.merge("RGBA", [
            Image.fromarray(r.astype(np.uint8)),
            Image.fromarray(g.astype(np.uint8)),
            Image.fromarray(b.astype(np.uint8)),
            alpha
        ])
        return image