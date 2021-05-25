import logic
import puzzle
import vars.config as cfg
import vars.constants as c
import tkinter as tk

class LeftView(tk.Frame):
    def __init__(self, root):
        #call super class (Frame) constructor
        tk.Frame.__init__(self, root)
        #save root layour for later references
        self.root = root
        #load all UI
        self.setup_ui()
        
    def setup_ui(self):
        #create a output label
        self.output_label = tk.Label(self, text="Webcam Output", bg="black", fg="white")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        #create label to hold image
        self.image_label = tk.Label(self)
        #put the image label inside left screen
        self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
        
    def update_image(self, image):
        #configure image_label with new image 
        self.image_label.configure(image=image)
        #this is to avoid garbage collection, so we hold an explicit reference
        self.image = image
    