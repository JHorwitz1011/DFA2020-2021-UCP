import numpy as np
from cv2 import cv2 as cv
from collections import deque

#Gamma Correction https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
def adjustGamma(image, gamma = 1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    
    return cv.LUT(image, table)

def horizontalFlip(image):
    return cv.flip(image,1)

# Setup
FRAME_WIDTH = 800
FRAME_HEIGHT = 800
MAXBUFFER = 64
GAMMA = 0.5

colorLower = (0, 200, 200)  # (29,86,6)
colorUpper = (10, 255, 255)  # (64,255,255)
pts = deque(maxlen=MAXBUFFER)


camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not camera.isOpened():
    print("Camera could not be referenced")
    exit(0)



#Frame processing
while True:
    ret, frame = camera.read()

    adjusted = adjustGamma(frame,GAMMA)

    frame = horizontalFlip(frame)
    adjusted = horizontalFlip(adjusted)
    
    cv.putText(adjusted,"Gamma = {}".format(GAMMA),(10,30),cv.FONT_HERSHEY_SIMPLEX, 0.8,(0,0,255),3)
    cv.imshow("Images", np.hstack([frame, adjusted]))

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break


cv.destroyAllWindows()
camera.release()