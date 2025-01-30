from PIL import Image
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('effects/faceOnly/haarcascade_frontalface_default.xml')

def findFaces(img):
    img = np.array(img.convert("RGB"))[:, :, ::-1]
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=0, minSize=(20, 20)
    )
    #faces = face_cascade.detectMultiScale(gray_image)
    for f in range(len(faces)):
        face = faces[f]
        faces[f] = (face[0] - (face[2] // 4), face[1] - (face[3] // 8), int(face[2] * 1.5), int(face[3] * 1.75))
    return faces

class Module:
    def __init__(self):
        self.name = "faceOnly"
        self.description = "Removes everything that's not a face"
        self.alpha = np.zeros((100, 100), dtype=np.uint8)

    def message(self, id, data):
        match id:
            case "dimensions":
                self.alpha = np.zeros((data[1], data[0]), dtype=np.uint8)
    
    def requestFrame(self, image):
        faces = findFaces(image)
        alpha = self.alpha.copy()
        for f in faces:
            # f = (x, y, width, height)
            alpha[f[1]:f[1] + f[3], f[0]:f[0] + f[2]] = 255
        image.putalpha(Image.fromarray(alpha))
        return image