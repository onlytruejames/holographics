from PIL import Image
import numpy as np
from components import VariableManager
import random

class Module:
    def __init__(self):
        self.name = "fadeVelocity"
        self.description = "Paste the previous frame behind this one at an offset determined by a velocity"
        self.variables = {
            "Constant": VariableManager("Constant", "boolean", False, "Is the velocity constant, or is it random?"),
            "Velocity": VariableManager("Velocity", "array", np.array([1, 1]), "The velocity of the offset. If the velocity is random, the first value is the maximum speed."),
            "Rate": VariableManager("Rate", "int", 5, "The amount of time taken for the acceleration to change"),
            "Fade": VariableManager("Fade", "integer", 10, "Specifies how much the image dims between frames")
        }
        self.acceleration = np.array([1, 0])
        self.velocity = np.array([1, 1])
        self.dimensions = (100, 100)
        self.lastImg = Image.new("RGBA", self.dimensions)

    def message(self, id, data):
        match id:
            case "variableUpdate":
                if data == "Velocity":
                    self.velocity = self.variables["Velocity"].value
            case "dimensions":
                self.dimensions = data
                self.lastImg = self.lastImg.resize(data, Image.NEAREST)

    def requestFrame(self, image):
        backImage = np.clip((np.array(self.lastImg).astype(np.int64) - self.variables["Fade"].value), 0, 255).astype(np.uint8)
        if not self.variables["Constant"].value:
            varVelocity = abs(self.variables["Velocity"].value[0])
            if random.randint(0, self.variables["Rate"].value) == 1:
                self.acceleration = np.array([random.randint(-2, 2), random.randint(-2, 2)])
            self.velocity += self.acceleration
            self.velocity = np.clip(self.velocity, -varVelocity, varVelocity)
        backImage = Image.fromarray(np.roll(backImage, self.velocity, (0, 1)))
        backImage.alpha_composite(image)
        self.lastImg = backImage.copy()
        return backImage