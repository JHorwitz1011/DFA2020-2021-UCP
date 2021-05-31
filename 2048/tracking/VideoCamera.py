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