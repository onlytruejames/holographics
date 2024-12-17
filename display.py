import tkinter as tk
from PIL import Image, ImageTk
from json import load
from classes import Slide

def loadProject(name):
    file = open(f"projects/{name}/project.json", "r")
    project = load(file)
    file.close()
    return project

project = loadProject(input("What is the name of the project you want to open?\n"))
global sequence
sequence = project["sequence"]
global slideIndex
slideIndex = -1
global currentSlide
currentSlide = None
global scale
try:
    scale = project["scale"]
except:
    scale = 1

window = tk.Tk() # Create Tk object

def refresh():
    # Whenever you update the window, do this to make the window reflect these changes
    window.update_idletasks()
    window.update()

img = ImageTk.PhotoImage(Image.new("RGB", (100, 100))) # Make placeholder image for the label
label = tk.Label(window, image=img)
label.pack() # Add to the window
refresh() # Update

def updateWindow(image):
    # https://stackoverflow.com/a/3482156/
    image = ImageTk.PhotoImage(image)
    label.configure(image=image)
    label.image = image # Tkinter weirdness means this is how you do it

def getWindowSize():
    # https://stackoverflow.com/a/4221002/
    return (window.winfo_screenwidth() // scale, window.winfo_screenheight() // scale)

windowSize = getWindowSize()

global blankImage
blankImage = Image.new("RGBA", windowSize, (0, 0, 0, 0)) # Create an empty transparent image to apply the first effect to
blackImage = Image.new("RGBA", windowSize, (0, 0, 0, 255)) # Create a black image to paste the image onto at the end
def getFrame():
    global windowSize
    if not getWindowSize() == windowSize:
        windowSize = getWindowSize()
        for eff in currentSlide.effects:
            eff.message("dimensions", windowSize)
    # Assuming a global variable for the slide and dimensions
    image = blankImage.copy()
    for eff in currentSlide.effects: # Iterate through all effects and process frames through all
        newImage = eff.requestFrame(image)
        # Decide how to composite the new and old frames together
        match eff.compositeMode:
            # At first I'm only supporting "front", "behind", and "replace".
            case "front":
                image = Image.alpha_composite(image, newImage)
            case "behind":
                image = Image.alpha_composite(newImage, image)
            case "replace":
                image = newImage
    black = blackImage.copy()
    black.paste(image)
    return black

global running
running = True # Variable for checking whether the program should still be running

def quit(x): # Blank variable because tkinter gives you one which we don't need
    global running
    window.quit() # Quit the window
    running = False # End the loop at the end of the program

def nextSlide():
    try:
        global slideIndex
        global currentSlide
        slideIndex += 1 # Increment by 1
        currentSlide = Slide() # Create slide
        currentSlide.load(sequence[slideIndex]) # Load into slide
        for eff in currentSlide.effects:
            eff.message("dimensions", windowSize) # Message to inform effects of dimensions
    except Exception as e:
        print(e)
        quit(1)

nextSlide()

window.attributes("-fullscreen", True) # Make the window fullscreen
window.bind("<Escape>", quit) # The window closes when you press escape now
window.bind("<Right>", lambda x: nextSlide()) # When you press the right arrow key the next slide should appear

while running:
    try:
        frame = getFrame() # Get the frame
        frame = frame.resize((windowSize[0] * scale, windowSize[1] * scale))
        updateWindow(frame) # Put the frame in the window
        refresh() # Remind the window that it's not rendering the frame
    except Exception as e:
        # An error occurred, print it for debugging purposes and quit safely
        print(e)
        quit(1)