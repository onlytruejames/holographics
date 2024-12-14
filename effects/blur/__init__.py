from components import EffectVariable
from PIL import ImageFilter
class Module:
    def __init__(self):
        self.name = "blur"
        self.description = "Blurs an image by a given amount"
        amount = EffectVariable("Amount", "float", 0, "Amount of Blurring")
        # Internally, amount controls the radius of the Box Blur
        # The radius is defined by the minimum dimension size / Amount
        self.dimensions = (100, 100)
        self.radius = 0
        self.variables = {"Amount": amount}
        self.blurObject = ImageFilter.BoxBlur(self.radius)
    def requestFrame(self, image):
        amount = self.variables["Amount"].value # Get the amount of blurring
        image = image.filter(self.blurObject)
        return image
    def message(self, id, data):
        match id:
            case "dimension":
                self.dimensions = data
                self.radius = min(self.dimensions[0], self.dimensions[1]) / self.variables["Amount"].value
                self.blurObject = ImageFilter.BoxBlur(self.radius)
                pass
            case "variableUpdate":
                if data == "Amount":
                    self.radius = min(self.dimensions[0], self.dimensions[1]) / self.variables["Amount"].value
                    self.blurObject = ImageFilter.BoxBlur(self.radius)