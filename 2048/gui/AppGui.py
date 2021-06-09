import vars.constants as c
from gui.GameGrid import GameGrid
from gui.RightView import RightView
import tkinter as tk
from PIL import Image
from PIL import ImageTk

class AppGui:
    def __init__(self):
        #initialize the gui toolkit
        self.root = tk.Tk()
        #set the geometry of the window
        #self.root.geometry("550x300+300+150")
        self.root['bg'] = c.BACKGROUND_COLOR_APP
        
        #set title of window
        self.root.title("Face Detection")
        
        #create left screen view
        #EDIT
        self.left_view = GameGrid(self.root)
        # self.left_view = LeftView(self.root)
        self.left_view.pack(side='left')
        
        #create right screen view
        self.right_view = RightView(self.root)
        self.right_view.pack(side='right')
        
        #define image width/height that we will use
        #while showing an image in webcam/neural network
        #output window
        self.image_width = c.WIN_SIZE
        self.image_height = c.WIN_SIZE
        
        #define the center of the cirlce based on image dimentions
        #this is the cirlce we will use for user focus
        self.circle_center = (int(self.image_width/2),int(self.image_height/4))
        #define circle radius
        self.circle_radius = 15
        #define circle color == red
        self.circle_color = (255, 0, 0)
        
        self.is_ready = True
        
    def launch(self):
        #start the gui loop to listen for events
        self.root.mainloop()
        
    def process_image(self, image):
        #resize image to desired width and height
        #image = image.resize((self.image_width, self.image_height),Image.ANTIALIAS)
        #image = cv2.resize(image, (self.image_width, self.image_height))
        
        #EDIT
        #image = cv2.flip(image, 1)
        
        #if image is RGB (3 channels, which means webcam image) then draw a circle on it
        #for user to focus on that circle to align face
        #if(len(image.shape) == 3):
        #    cv2.circle(image, self.circle_center, self.circle_radius, self.circle_color, 2)
            
        #convert image to PIL library format which is required for Tk toolkit
        image = Image.fromarray(image)
        
        #convert image to Tk toolkit format
        image = ImageTk.PhotoImage(image)
        
        return image
        
    def update_webcam_output(self, image):
        #pre-process image to desired format, height etc.
        image = self.process_image(image)

        #pass the image to left_view to update itself
        self.left_view.update_image(image)
        
    def display_img_to_gui(self, image):
        #pre-process image to desired format, height etc.
        image = self.process_image(image)
        #pass the image to right_view to update itself
        self.right_view.update_image(image)
        
    def update_chat_view(self, question, answer_type):
        self.left_view.update_chat_view(question, answer_type)
        
    def update_emotion_state(self, emotion_state):
        self.right_view.update_emotion_state(emotion_state)
    