from queue import Queue
from WebcamThread import WebcamThread

class Wrapper:
    def __init__(self):
        self.app_gui = AppGui()
        
        #create a Video camera instance
        #self.camera = VideoCamera()
        
        #intialize variable to hold current webcam video frame
        self.current_frame = None
        
        #create a queue to fetch and execute callbacks passed 
        #from background thread
        self.frame_queue = Queue()
        self.input_queue = Queue()

        #create a thread to fetch webcam feed video
        self.webcam_thread = WebcamThread(self.app_gui, self.frame_queue)
        
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