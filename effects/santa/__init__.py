from PIL import Image
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('effects/santa/haarcascade_frontalface_default.xml')

nicholas = Image.open("effects/santa/nicholas.png")

def findFaces(img):
    img = np.array(img.convert("RGB"))[:, :, ::-1]
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_classifier.detectMultiScale(
    #    gray_image, scaleFactor=1.4, minNeighbors=1, minSize=(1, 1)
    #)
    faces = face_cascade.detectMultiScale(gray_image)
    for f in range(len(faces)):
        face = faces[f]
        faces[f] = (face[0] - (face[2] // 4), face[1] - (face[3] // 8), int(face[2] * 1.5), int(face[3] * 1.75))
    return faces

class Module:
    def __init__(self):
        self.name = "santa"
        self.description = "Adds santa hats and beards to everyone in the frame"
    
    def requestFrame(self, image):
        faces = findFaces(image)
        for f in faces:
            thisSanta = nicholas.resize((f[2], f[3]))
            image.alpha_composite(thisSanta, (f[0], f[1]))
        return image