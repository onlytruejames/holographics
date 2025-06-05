from components import VariableManager
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from cv2.videoio_registry import getBackendName
from PIL import Image
from cv2_enumerate_cameras import enumerate_cameras

class CameraRegistry:
    def __init__(self):
        self.search()
        self.using = {}
    
    def search(self):
        cameras = {}
        for cam in enumerate_cameras():
            if not cam.name in cameras:
                cameras[cam.name] = []
            cameras[cam.name].append({
                "index": cam.index,
                "backend": cam.backend
            })
        self.cameras = cameras

    def open(self, name):
        self.search()
        if name in self.cameras:
            for camera in self.cameras[name]:
                try:
                    #print(f"{name}: Trying index {camera['index']} with backend {camera['backend']}")
                    self.using[name] = VideoCapture(camera["index"], camera["backend"])
                    success, image = self.using[name].read()
                    if success:
                        print(f"Successfully opened {name}")
                        break
                except:
                    continue
        else:
            print(f"Camera '{name}' not found, using default instead")
            self.using[name] = VideoCapture(0)
    
    def close(self, name):
        if name in self.using:
            self.using[name].release()
            self.using.pop(name)
    
    def snap(self, name):
        if not name in self.using:
            self.open(name)
        return self.using[name].read()

Manager = CameraRegistry()

class Module:
    def __init__(self):
        self.name = "camera"
        self.description = "Use a webcam as a source"
        self.dimensions = [100, 100] # default
        self.blankImage = None # I will assign this later, this won't be accessed before
        self.cameraName = ""
        # Assign variables as an attribute so it is externally available
        self.variables = {
            "Preserve Aspect Ratio": VariableManager("Preserve Aspect Ratio", "boolean", True, "When resizing the camera photo, preserve the aspect ratio?"),
            "Camera Name": VariableManager("Camera Name", "string", None, "The name of the camera you want to use. If not available, the first detected camera will be used.")
        }
        # Below are relevant variables to zoomToFit
        self.resizeDims = None # Dimensions the camera photo is resized to
        self.resizeCoordinate = [0, 0] # And the coordinate it is pasted onto

    def requestFrame(self, image):
        # The image parameter is not used
        success, cameraPicture = Manager.snap(self.cameraName)
        if not success:
            return image # As opposed to crashing
        cameraPicture = cvtColor(cameraPicture, COLOR_BGR2RGB)
        cameraPicture = Image.fromarray(cameraPicture).convert("RGBA") # Convert to PIL format
        # There will likely be a conversion to get this image into the PIL format
        preservesAR = self.variables["Preserve Aspect Ratio"].value # Is the aspect ratio being preserved?
        if not preservesAR:
            cameraPicture = cameraPicture.resize(self.dimensions, Image.NEAREST)
            return cameraPicture
        else:
            cameraPicture = cameraPicture.resize(self.resizeDims, Image.NEAREST)
            # Paste onto blank image at the correct coordinates to centre the camera photo
            blank = self.blankImage.copy()
            blank.paste(cameraPicture, self.resizeCoordinate)
            return blank
    
    def dimensionConfig(self):
        try:
            # First we compare the aspect ratios of the media file and the 
            # requested dimensions. Aspect ratio is width / height, which can be 
            # interpreted as the wideness of an image.
            success, examplePhoto = Manager.snap(self.cameraName) # More reliable way of testing dimensions than using attributes
            # Cameras are annoyingly non-standardised.
            examplePhoto = cvtColor(examplePhoto, COLOR_BGR2RGB)
            examplePhoto = Image.fromarray(examplePhoto) # Convert to PIL format
            camWidth = examplePhoto.width
            camHeight = examplePhoto.height
            camAspectRatio = camWidth / camHeight
            dimAspectRatio = self.dimensions[0] / self.dimensions[1]
            if camAspectRatio > dimAspectRatio:
                # Media is wider than the dimensions, proportionally.
                width = self.dimensions[0] # The camera image will be the width of the dimensions.
                # Media width / Dimensions width = Media height / Dimensions  height. So output height = Media height * (Dimensions width /  Media width)
                height = camHeight * (self.dimensions[0] / camWidth)
            else:
                # The opposite of the previous part
                height = self.dimensions[1]
                width = camWidth * (self.dimensions[1] / camHeight)
            self.resizeDims = (int(width), int(height))
            coordinate = (
                (self.blankImage.width - self.resizeDims[0]) // 2,
                (self.blankImage.height - self.resizeDims[1]) // 2
            ) # Halfway between (0, 0) and the difference between the dimensions 
            # results in a centred placement. Also rounded to be an integer.
            self.resizeCoordinate = coordinate
        except:
            pass

    def message(self, id, data):
        print(f"CAMERA - id: {id}, data: {data}")
        match id: # Decide what to do with the message based on its identifier
            case "variableUpdate":
                if data == "Camera Name":
                    Manager.close(self.cameraName)
                    self.cameraName = self.variables["Camera Name"].value
                    Manager.open(self.cameraName)
                    self.dimensionConfig()

            case "dimensions":
                self.dimensions = data
                self.blankImage = Image.new("RGBA", self.dimensions, (0, 0, 0, 0))
                self.dimensionConfig()

            case "slideEnd":
                Manager.close(self.cameraName)