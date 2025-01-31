import tkinter as tk
from PIL import Image, ImageTk
from json import load
from classes import Slide
import numpy as np

class DisplayWindow:
    def __init__(self, name, debugging=False):
        file = open(f"projects/{name}/project.json", "r")
        self.project = load(file)
        self.sequence = self.project["sequence"]
        self.slideIndex = 0
        file.close()
        try:
            self.scale = self.project["scale"]
        except:
            self.scale = 1
        self.debugging = debugging
        self.sequence = self.project["sequence"]
        self.currentSlide = None
        self.running = True # Variable for checking whether the program should still be running

        self.window = tk.Tk() # Create Tk object
        self.window.configure(bg='black')
        img = ImageTk.PhotoImage(Image.new("RGB", (100, 100))) # Make placeholder image for the label
        self.label = tk.Label(self.window, image=img)
        self.label.pack() # Add to the window
        self.window.attributes("-fullscreen", True) # Make the window fullscreen
        self.window.bind("<Escape>", self.quit) # The window closes when you press escape now
        self.window.bind("<Right>", self.nextSlide) # When you press the right arrow key the next slide should appear

        self.refresh() # Update
        self.windowSize = self.getWindowSize()

        self.blankImage = Image.new("RGBA", self.windowSize, (0, 0, 0, 0)) # Create an empty transparent image to apply the first effect to
        self.blackImage = Image.new("RGBA", self.windowSize, (0, 0, 0, 255)) # Create a black image to paste the image onto at the end
        
        self.createSlide()

    def getFrame(self):
        # this is the first time i've used the walrus operator :) :) :) :) :)
        if not (newSize := self.getWindowSize()) == self.windowSize:
            windowSize = newSize
            for eff in self.currentSlide.effects:
                eff.message("dimensions", windowSize)
            self.blankImage = Image.new("RGBA", self.windowSize, (0, 0, 0, 0)) # Create an empty transparent image to apply the first effect to
            self.blackImage = Image.new("RGBA", self.windowSize, (0, 0, 0, 255)) # Create a black image to paste the image onto at the end
        
        image = self.blankImage.copy()
        for eff in self.currentSlide.effects: # Iterate through all effects and process frames through all
            newImage = eff.requestFrame(image).copy()
            image = eff.merger.merge(image, newImage).copy()
        black = self.blackImage.copy()
        black.alpha_composite(image)
        return black

    def quit(self, x=None): # Blank variable because tkinter gives you one which we don't need
        self.window.quit() # Quit the window
        self.running = False # End the loop at the end of the program

    def refresh(self):
        # Whenever you update the window, do this to make the window reflect these changes
        self.window.update_idletasks()
        self.window.update()
    
    def updateWindow(self, image):
        # https://stackoverflow.com/a/3482156/
        image = ImageTk.PhotoImage(image)
        self.label.configure(image=image)
        self.label.image = image # Tkinter weirdness means this is how you do it
    
    def getWindowSize(self):
        # https://stackoverflow.com/a/4221002/
        return (self.window.winfo_screenwidth() // self.scale, self.window.winfo_screenheight() // self.scale)

    def createSlide(self):
        newSlide = Slide() # Create slide
        newSlide.load(self.sequence[self.slideIndex]) # Load into slide
        for eff in newSlide.effects:
            eff.message("dimensions", self.windowSize) # Message to inform effects of dimensions
        self.currentSlide = newSlide
    
    def nextSlide(self, x=None):
        for eff in self.currentSlide.effects:
                eff.message("slideEnd", "") # Message to inform effects of dimensions
        self.slideIndex += 1 # Increment by 1
        try:
            self.createSlide()
        except Exception as e:
            self.quit()
            raise e    
    
    def run(self):
        while self.running:
            try:
                frame = self.getFrame() # Get the frame
                frame = frame.resize((self.windowSize[0] * self.scale, self.windowSize[1] * self.scale), Image.NEAREST)
                self.updateWindow(frame) # Put the frame in the window
                self.refresh() # Remind the window that it's not rendering the frame
            except Exception as e:
                # An error occurred, quit safely before raising the error
                self.quit()
                raise e

if __name__ == "__main__":
    root = DisplayWindow(input("What is the name of the project you want to open?\n"))
    root.run()