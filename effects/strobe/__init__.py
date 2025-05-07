import numpy as np
from PIL import Image
from components import VariableManager
class Module:
    def __init__(self):
        self.name = "strobe"
        self.description = "Create a strobing effect"
        amount = VariableManager("Amount", "float", 0, "(0-1): The intensity of the strobing effect")
        frequency = VariableManager("Frequency", "integer", 10, "The number of frames it takes for the strobe effect to cycle once")
        self.variables = {"Amount": amount, "Frequency": frequency}
        self.phase = 0

    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = np.array(image) # Use numpy in my case to turn the image into a 2D array
        self.phase += 1
        freq = self.variables["Frequency"].value
        amount = self.variables["Amount"].value
        self.phase = self.phase % freq
        multiplier = (1 - amount) + (self.phase/freq) * amount
        # For this frame, this is the amount the brightness needs multiplying by
        image = image * multiplier # Produce brightness result
        image = image.astype(np.uint8) # Ensure that all pixel values are integers
        image = Image.fromarray(image) # Convert back into image datatype
        image.putalpha(alpha)
        return image