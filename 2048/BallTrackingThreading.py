# coding: utf-8

# # Application GUI

# In[1]:
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import threading
import queue
import time

import sys
from tkinter import Frame, Label, CENTER
import random
import keyboard 

import logic
import constants as c

# Ball Tracking
from collections import deque
from imutils.video import VideoStream
import imutils
import numpy as np

WIN_SIZE = W = H =  700
#H = (W // 4) * 3

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#orangeLower = (0, 220, 158)
#orangeUpper = (12, 255, 255)
colorUpper = (0,0,0)
colorLower = (0,0,0)

orangeLower = (0, 130, 130)
orangeUpper = (19, 255, 255)   
yellowLower= (20, 100, 125)
yellowUpper= (255, 255, 255)   
blueLower= (100,75, 100)
blueUpper= (255, 255, 255)

###constants###   
maxlen=10   
threshold = 150 
LINE_RED = (0, 0, 255)
LINE_GREEN = (0, 255, 0)

##variables##
cooldown = 0
pts = deque(maxlen=maxlen) 

last_input = False

LINE_THICKNESS = 64

## FPS
currentTime = 0
nextTime = 0
firstFrame= True

# I have taken a more modular approach so that UI is easy to change, update and extend. I have also developed UI in a way so that UI has no knowledge of how data is fetched or processed, it is just a UI. 

# ## Left Screen Views


class GameGrid(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self, root)
        self.root = root

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right,
                         c.KEY_H: logic.left, c.KEY_L: logic.right,
                         c.KEY_K: logic.up, c.KEY_J: logic.down}
        
        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        #self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                                                    fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2

# In[3]:

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
    


# ## Right Screen Views

# In[5]:

class RightView(tk.Frame):
    def __init__(self, root):
        #call super class (Frame) constructor
        tk.Frame.__init__(self, root)
        #save root layour for later references
        self.root = root
        #load all UI
        self.setup_ui()
        
    def setup_ui(self):
        #create a webcam output label
        #EDIT

        self.output_label = tk.Label(self, text="Color Ball Tracking", bg="white", fg="black")
        self.output_label.pack(side="top", fill="both", expand="yes", padx=10)
        
        #create label to hold image
        self.image_label = tk.Label(self)
        #put the image label inside left screen
        self.image_label.pack(side="left", fill="both", expand="yes", padx=10, pady=10)
        self.selection_frame = tk.Frame(self,bg='gray')

        self.selected_color = 100
        self.orange_button = tk.Radiobutton(self.selection_frame, text='      ', value=0,
            command=self.orange_callback, bg='orange')
        self.orange_button.pack()
        
        self.blue_button = tk.Radiobutton(self.selection_frame, text='      ',value=1,
                                          command=self.blue_callback, bg='blue', )
        self.blue_button.pack()

        self.yellow_button = tk.Radiobutton(self.selection_frame, text='      ',value=2,
                                          command=self.yellow_callback, bg='yellow', )
        self.yellow_button.pack()

        self.selection_frame.pack()

    def orange_callback(self):
        global colorUpper, colorLower
        colorUpper = orangeUpper
        colorLower = orangeLower
    
    def blue_callback(self):
        global colorUpper, colorLower
        colorUpper = blueUpper
        colorLower = blueLower  
    def yellow_callback(self):
        global colorUpper, colorLower
        colorUpper = yellowUpper
        colorLower = yellowLower    
    def update_image(self, image):
        #configure image_label with new image 
        self.image_label.configure(image=image)
        #this is to avoid garbage collection, so we hold an explicit reference
        self.image = image
        


# ## All App GUI Combined

# In[6]:

class AppGui:
    def __init__(self):
        #initialize the gui toolkit
        self.root = tk.Tk()
        #set the geometry of the window
        #self.root.geometry("550x300+300+150")
        
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
        self.image_width=WIN_SIZE
        self.image_height=WIN_SIZE
        
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
        
    def update_neural_network_output(self, image):
        #pre-process image to desired format, height etc.
        image = self.process_image(image)
        #pass the image to right_view to update itself
        self.right_view.update_image(image)
        
    def update_chat_view(self, question, answer_type):
        self.left_view.update_chat_view(question, answer_type)
        
    def update_emotion_state(self, emotion_state):
        self.right_view.update_emotion_state(emotion_state)
    


# ## Class to Access Webcam

# In[7]:

import cv2

class VideoCamera:
    def __init__(self):
        #passing 0 to VideoCapture means fetch video from webcam
        self.video_capture = cv2.VideoCapture(0)
                
    #release resources like webcam
    def __del__(self):
        self.video_capture.release()
        
    def read_image(self):
        #get a single frame of video
        ret, frame = self.video_capture.read()
        #return the frame to user
        return ret, frame
    
    #method to release webcam manually 
    def release(self):
        self.video_capture.release()
        
#function to detect face using OpenCV
def detect_face(img):
    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow Haar classifier
    face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')
    
    #img_copy = np.copy(colored_img)
    
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    #if no faces are detected then return original img
    if (len(faces) == 0):
        return img
    
    #under the assumption that there will be only one face,
    #extract the face area
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return img[y:y+w, x:x+h]


def press(input, key='a'):
        global cooldown
        global last_input
        if input and not last_input:
                keyboard.press_and_release(key)
                cooldown = 50
        last_input = input

#EDIT
#function to detect Aruco with OpenCV
def detect_color(img, points):
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    timeCheck = time.time()
    global cooldown
    if cooldown > 0:
        print(cooldown)
   
    # resize the img, blur it, and convert it to the HSV
    # color space
    img = imutils.resize(img, width=600) 
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                    # draw the circle and centroid on the img,
                    # then update the list of tracked points
                    cv2.circle(img, (int(x), int(y)), int(radius),
                                        (0, 255, 255), 2)
                    cv2.circle(img, center, 5, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)

    if(len(pts) == maxlen and pts[maxlen-1] is not None and pts[0] is not None):
            #print('left:', pts[0])
            #print('right:', pts[maxlen-1])
            xdif = pts[maxlen-1][0] - pts[0][0]
            #print('xdif:', xdif)
            ydif = pts[maxlen-1][1] - pts[0][1]
            #print('ydif:', ydif)
            if xdif > threshold:
                    print('RIGHT')
                    press(True, key='d')
            elif xdif < -1 * threshold:
                    print('LEFT')
                    press(True, key='a')
            elif ydif > threshold:
                    print('UP')
                    press(True, key='w')
            elif ydif < -1 * threshold:
                    print('DOWN')
                    press(True, key='s')
            else:
                    press(False)


        # loop over the set of tracked points
    for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                    continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(LINE_THICKNESS/ float(i + 1)) * 2.5)
            if last_input or cooldown > 0:
                    cv2.line(img, pts[i - 1], pts[i], LINE_GREEN, thickness)
                    if cooldown > 0:
                            cooldown -= 1
            else:
                    cv2.line(img, pts[i - 1], pts[i], LINE_RED, thickness)

    img = cv2.flip(img, 1)

    #Adjust Framerate
    frameRate = 1 / (time.time() - timeCheck) 
    print(frameRate)

    #if(frameRate >30):
        


    return img

    

# ## Thread Class for Webcam Feed

# In[8]:

class WebcamThread(threading.Thread):
    def __init__(self, app_gui, callback_queue):
        #call super class (Thread) constructor
        threading.Thread.__init__(self)
        #save reference to callback_queue
        self.callback_queue = callback_queue
        
        #save left_view reference so that we can update it
        self.app_gui = app_gui
        
        #set a flag to see if this thread should stop
        self.should_stop = False
        
        #set a flag to return current running/stop status of thread
        self.is_stopped = False
        
        #create a Video camera instance
        self.camera = VideoCamera()
        
    #define thread's run method
    def run(self):
        #start the webcam video feed
        while (True):
            #check if this thread should stop
            #if yes then break this loop
            if (self.should_stop):
                self.is_stopped = True
                break
            

            #read a video frame
            ret, self.current_frame = self.camera.read_image()

            if(ret == False):
                print('Video capture failed')
                exit(-1)
                
            #opencv reads image in BGR color space, let's convert it 
            #to RGB space
            self.current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            #key = cv2.waitKey(10)
            
            if self.callback_queue.full() == False:
                #put the update UI callback to queue so that main thread can execute it
                self.callback_queue.put((lambda: self.update_on_main_thread(self.current_frame, self.app_gui)))

        
        #fetching complete, let's release camera
        #self.camera.release()
        
            
    #this method will be used as callback and executed by main thread
    def update_on_main_thread(self, current_frame, app_gui):
        #app_gui.update_webcam_output(current_frame)
        #face = detect_face(current_frame)
        #EDIT
        face = detect_color(current_frame, pts)
        app_gui.update_neural_network_output(face)
        
    def __del__(self):
        self.camera.release()
            
    def release_resources(self):
        self.camera.release()
        
    def stop(self):
        self.should_stop = True
    
        


# ## A GUI Wrappr (Interface) to Connect it with Data

# In[9]:

class Wrapper:
    def __init__(self):
        self.app_gui = AppGui()
        
        #create a Video camera instance
        #self.camera = VideoCamera()
        
        #intialize variable to hold current webcam video frame
        self.current_frame = None
        
        #create a queue to fetch and execute callbacks passed 
        #from background thread
        self.callback_queue = queue.Queue()
        
        #create a thread to fetch webcam feed video
        self.webcam_thread = WebcamThread(self.app_gui, self.callback_queue)
        
        #save attempts made to fetch webcam video in case of failure 
        self.webcam_attempts = 0
        
        #register callback for being called when GUI window is closed
        self.app_gui.root.protocol("WM_DELETE_WINDOW", self.on_gui_closing)
        
        #start webcam
        self.start_video()
        
        #start fetching video
        self.fetch_webcam_video()
    
    def on_gui_closing(self):
        self.webcam_attempts = 51
        self.webcam_thread.stop()
        self.webcam_thread.join()
        self.webcam_thread.release_resources()
        
        self.app_gui.root.destroy()

    def start_video(self):
        self.webcam_thread.start()
        
    def fetch_webcam_video(self):
            try:
                #while True:
                #try to get a callback put by webcam_thread
                #if there is no callback and call_queue is empty
                #then this function will throw a Queue.Empty exception 
                callback = self.callback_queue.get_nowait()
                callback()
                self.webcam_attempts = 0
                #self.app_gui.root.update_idletasks()
                self.app_gui.root.after(7, self.fetch_webcam_video)
                    
            except queue.Empty:
                if (self.webcam_attempts <= 500):
                    self.webcam_attempts = self.webcam_attempts + 1
                    self.app_gui.root.after(10, self.fetch_webcam_video)

    def test_gui(self):
        #test images update
        #read the images using OpenCV, later this will be replaced
        #by live video feed
        image, gray = self.read_images()
        self.app_gui.update_webcam_output(image)
        self.app_gui.update_neural_network_output(gray)
        
        #test chat view update
        self.app_gui.update_chat_view("4 + 4 = ? ", "number")
        
        #test emotion state update
        self.app_gui.update_emotion_state("neutral")
        
    def read_images(self):
        image = cv2.imread('data/test1.jpg')
    
        #conver to RGB space and to gray scale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        return image, gray
    
    def launch(self):
        self.app_gui.launch()
        
    def __del__(self):
        print('Done')#EDIT self.webcam_thread.stop()




# ## The Launcher Code For GUI

# In[10]:

# if __name__ == "__main__":


wrapper = Wrapper()
wrapper.launch()
