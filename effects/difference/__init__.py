# Return the difference between two frames. This module can be setup as a storer, a comparer, or a storer and comparer.
from PIL import Image
import numpy as np
from components import VariableManager

global directory
directory = {}

class Module:
    def __init__(self):
        self.name = "difference"
        self.description = "Return the difference between two frames. This module can be setup as a storer, a comparer, or a storer and a comparer."
        mode = VariableManager("Mode", "string", "Store/Compare", "Whether this module is a storer, a comparer, or a storer and a comparer.")
        id = VariableManager("Id", "string", "beanchester united", "The identifier which links up storers and comparers and their relevant data. If an identifier has no associated image when compared against, a storer becomes a comparer.")
        self.variables = {
            "Mode": mode,
            "Id": id,
        }
    
    def requestFrame(self, image):
        alpha = image.getchannel("A")
        image = np.array(image).astype(np.int16)
        id = self.variables["Id"].value
        if not id in directory:
            directory[id] = image
            return Image.fromarray(image.astype(np.uint8))
        match self.variables["Mode"].value:
            case "Store":
                directory[id] = image
                return Image.fromarray(image.astype(np.uint8))
            case "Compare":
                image = image - directory[id]
                image = np.abs(image)
            case "Store/Compare":
                oldVal = directory[id]
                directory[id] = image
                image = image - oldVal
                image = np.abs(image)
            case "Compare/Store":
                oldVal = directory[id]
                directory[id] = image
                image = image - oldVal
                image = np.abs(image)
        image = np.clip(image, 0, 255)
        newImage = Image.fromarray(image.astype(np.uint8))
        newImage.putalpha(alpha)
        return newImage
    
    def message(self, id, data):
        match id:
            case "dimensions":
                for key in directory:
                    directory[key] = directory[key].resize(data, Image.NEAREST)