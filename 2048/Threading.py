# coding: utf-8

# # Application GUI

# In[1]:

import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import threading
import queue

import sys
from tkinter import Frame, Label, CENTER
import random
import keyboard 

import logic
import constants as c

WIN_SIZE = W = 700
H = (W // 4) * 3
TAG_TYPE = "DICT_ARUCO_ORIGINAL"
UP_LINE = H//4    #cv2.rectangle(frame, (W // 4, H // 4), ((W // 4) * 3, (H // 4) * 3), (0, 0, 255), 3)
DOWN_LINE = (H // 4) * 3
LEFT_LINE = W // 4
RIGHT_LINE = (W // 4) * 3

FRAMES = 15 #velocity??
up_frames = down_frames = left_frames = right_frames = 0


ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}
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
        self.output_label = tk.Label(self, text="Aruco Tracking", bg="black", fg="white")
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
        image = cv2.resize(image, (self.image_width, self.image_height))
        
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

#EDIT
#function to detect Aruco with OpenCV
def detect_aruco(img):
    global up_frames, down_frames, left_frames, right_frames

    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[TAG_TYPE])
    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters = arucoParams)
    cv2.aruco.drawDetectedMarkers(img,corners,ids,(0,255,0))
    
    img = cv2.flip(img, 1) 

    if len(corners) > 0:
        img = cv2.flip(img, 1) 
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            
            # compute and draw the center (x, y)-coordinates of the ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            
            #Flip before text is written
            img = cv2.flip(img, 1) 

            # draw the ArUco marker ID on the frame - topLeft[0], topLeft[1] - 15
            cv2.putText(img, "MarkerID " + str(markerID), (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            if cY < UP_LINE:
                cv2.putText(img, "Up" + str(up_frames), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                up_frames += 1
            elif cY > DOWN_LINE:
                cv2.putText(img, "Down" + str(down_frames), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                down_frames += 1
            
      
            if cX > RIGHT_LINE:
                cv2.putText(img, "Left" + str(left_frames), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                left_frames += 1
            elif cX < LEFT_LINE:
                cv2.putText(img, "Right" + str(right_frames), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                right_frames += 1        
            
            if up_frames > FRAMES:
                keyboard.press_and_release('w')
                up_frames = 0

            elif down_frames > FRAMES:
                keyboard.press_and_release('s')
                down_frames = 0

            elif left_frames > FRAMES:
                keyboard.press_and_release('a')
                left_frames = 0

            elif right_frames > FRAMES:
                keyboard.press_and_release('d')
                right_frames = 0     

    cv2.line(img, (0,UP_LINE), (W, UP_LINE), (0,255,0),2)
    cv2.line(img, (0, DOWN_LINE), (W, DOWN_LINE), (0,255,0),2)
    cv2.line(img, (LEFT_LINE,0 ), (LEFT_LINE, H), (0,255,0),2)
    cv2.line(img, (RIGHT_LINE, 0), (RIGHT_LINE, H), (0,255,0),2)

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
        face = detect_aruco(current_frame)
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
                self.app_gui.root.after(70, self.fetch_webcam_video)
                    
            except queue.Empty:
                if (self.webcam_attempts <= 50):
                    self.webcam_attempts = self.webcam_attempts + 1
                    self.app_gui.root.after(100, self.fetch_webcam_video)

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
