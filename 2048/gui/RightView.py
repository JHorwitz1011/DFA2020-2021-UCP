import tkinter as tk
import vars.constants as c
import vars.config as cfg
#from gui.GameGrid import *
import shelve
import cv2
from collections import deque

from tracking.Tracking import auto_range
class RightView(tk.Frame):
    def __init__(self, root):
        #call super class (Frame) constructor
        tk.Frame.__init__(self, root)
        #save root layour for later references
        self.root = root
        #load all UI
        self.setup_ui()
        self['bg'] = c.BACKGROUND_COLOR_APP

    def setup_ui(self):
        #create a webcam output label
        #EDIT

        self.output_label = tk.Label(self, text="Color Ball Tracking", bg=c.BACKGROUND_COLOR_APP, fg="white")
        self.output_label.pack(side=tk.TOP, fill="both", expand="yes", padx=10)
        
        #create label to hold image
        self.image_label = tk.Label(self)
        #put the image label inside left screen
        self.image_label.pack(side=tk.TOP, fill="both", expand="yes", padx=10, pady=10)
        self.selection_frame = tk.Frame(self,bg=c.BACKGROUND_COLOR_APP)

        #color data
        #self.selected_color = tk.StringVar()    #Tkinter needs this variable type for the buttons, seems to be an enum type
 
        # self.orange_button = tk.Radiobutton(self.selection_frame, text='      ', value='orange',
        #                                     command=self.button_callback, bg='orange', variable = self.selected_color, height = c.BUTTON_HEIGHT )
        # self.orange_button.pack(side = tk.LEFT)
        
        # self.blue_button = tk.Radiobutton(self.selection_frame, text='      ',value='blue',
        #                                     command=self.button_callback, bg='blue',variable = self.selected_color, height = c.BUTTON_HEIGHT )
        # self.blue_button.pack(side = tk.LEFT)

        # self.yellow_button = tk.Radiobutton(self.selection_frame, text='      ',value='yellow',
        #                                     command=self.button_callback, bg='yellow',variable = self.selected_color, height = c.BUTTON_HEIGHT )
        # self.yellow_button.pack(side = tk.LEFT)

        # self.magenta_button = tk.Radiobutton(self.selection_frame, text='      ', value = 'magenta',
        #                                     command = self.button_callback, bg = 'magenta', variable = self.selected_color , height = c.BUTTON_HEIGHT )
        # self.green_button = tk.Radiobutton(self.selection_frame, text='      ', value = 'green',
        #                                     command = self.button_callback, bg = 'green', variable = self.selected_color, height = c.BUTTON_HEIGHT )
        # self.magenta_button.pack(side = tk.LEFT)
        # self.green_button.pack(side = tk.LEFT)
        
        #self.selected_color.set(cfg.color)
        #self.button_callback()

        self.slider = tk.Scale(self.selection_frame, bg = c.BACKGROUND_COLOR_APP, highlightbackground = c.BACKGROUND_COLOR_APP ,from_=50, to_=250, command=self.slider_callback, orient = tk.HORIZONTAL, length = 200, width = 25, fg='white' )
        self.slider.set(cfg.threshold)
        self.slider.pack(side = tk.LEFT, expand = tk.YES)


        self.selection_frame.pack(side = tk.TOP, expand =tk.YES)

        # Restart
        self.restart = tk.Button(self.selection_frame, text ="Restart", command = self.restartCallback)
        self.restart.pack(side = tk.LEFT)

        # Calibrate 
        self.calibrate = tk.Button(self.selection_frame, text ="Calibrate", command = self.calibrateCallback)
        self.calibrate.pack(side = tk.LEFT)

        # Pause Tracking
        self.tracking_enabled_var = tk.BooleanVar(value=cfg.tracking_enabled)
        self.tracking_enabled = tk.Checkbutton(self.selection_frame, text ="Tracking", command = self.tracking_enabled_callback, variable=self.tracking_enabled_var)
        self.tracking_enabled.pack(side = tk.LEFT)

        # Scoring
        self.currentScoreLabel = tk.Label(self.selection_frame, text="Current Score: "+str(cfg.currentScore), bg=c.BACKGROUND_COLOR_APP, fg="white")
        self.currentScoreLabel.pack(side=tk.BOTTOM, fill="both", expand="yes", padx=10)

        self.highScoreLabel = tk.Label(self.selection_frame, text="High Score: "+str(cfg.highScore), bg=c.BACKGROUND_COLOR_APP, fg="white")
        self.highScoreLabel.pack(side=tk.BOTTOM, fill="both", expand="yes", padx=10)

    # Scoring
    def setCurrentScore(self, value):
        self.currentScoreLabel.config(text = "Current Score: "+str(value))
    
    def setHighScore(self):
        self.highScoreLabel.config(text= "High Score: " + str(cfg.currentScore))

    #Restart
    def restartCallback(self):

        # yikes. required to avoid a cyclic import error if import is placed at the top of the file
        from gui.GameGrid import GameGrid
        GameGrid.restart(cfg.wrapper.app_gui.left_view)

    def calibrateCallback(self):
        cfg.recalibrate = True
    
    def tracking_enabled_callback(self):
        if not self.tracking_enabled_var.get():
            cfg.pts = deque(maxlen=c.maxlen)
        cfg.tracking_enabled = self.tracking_enabled_var.get()


    def slider_callback(self, value):
        cfg.threshold = int(value)

        with shelve.open(c.filePath) as dataFile:
            dataFile['threshold'] = cfg.threshold
            #dataFile['color'] = 'blue'         ###############################################

        # print('slider callback works', value, self)

    # def button_callback(self):
    #     #string manipulation with a dictionary to get around having a large amount of callback methods
    #     #print('button callback')
    #     cfg.colorUpper = c.color_presets[self.selected_color.get() + "Upper"]
    #     cfg.colorLower = c.color_presets[self.selected_color.get() + "Lower"]
    #     with shelve.open(c.filePath) as dataFile:
    #         dataFile['color'] = self.selected_color.get()

    def update_image(self, image):
        #configure image_label with new image 
        self.image_label.configure(image=image)
        #this is to avoid garbage collection, so we hold an explicit reference
        self.image = image