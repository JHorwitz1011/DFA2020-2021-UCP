import threading
from tracking.VideoCamera import VideoCamera
from tracking.Tracking import *
import vars.config as cfg
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
        if cfg.recalibrate:
            cfg.recalibrate = False
            converted = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB) #Image taken from webcam in BGR
            converted = cv2.flip(converted, 1)
            c.color_presets['yellowLower'], c.color_presets['yellowUpper'] =roi_range(converted)
            cfg.colorLower = c.color_presets['yellowLower']
            cfg.colorUpper = c.color_presets['yellowUpper']

        face = detect_color(current_frame, cfg.pts)
        app_gui.update_neural_network_output(face)
        
    def __del__(self):
        self.camera.release()
            
    def release_resources(self):
        self.camera.release()
        
    def stop(self):
        self.should_stop = True