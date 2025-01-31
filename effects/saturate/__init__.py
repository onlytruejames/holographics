from components import VariableManager
from PIL import ImageEnhance
class Module:
    def __init__(self):
        self.name = "saturation"
        self.description = "Saturates an image by a given amount"
        amount = VariableManager("Amount", "float", 2, "Amount of Saturation")
        self.variables = {"Amount": amount}
    def requestFrame(self, image):
        amount = self.variables["Amount"].value # Get the amount of saturation
        converter = ImageEnhance.Color(image)
        saturatedImage = converter.enhance(amount)
        return saturatedImage