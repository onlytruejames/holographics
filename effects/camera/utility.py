from cv2_enumerate_cameras import enumerate_cameras

print("This is a list of your connnected cameras detectable by Holographics:")
for cam in enumerate_cameras():
    print(cam.name)

print("By specifying the camera name in your project.json file, you can choose which camera to use")