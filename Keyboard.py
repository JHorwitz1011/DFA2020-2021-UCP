
#https://www.pyimagesearch.com/2020/12/21/detecting-aruco-markers-with-opencv-and-python/

from imutils.video import VideoStream
import imutils
import time
from cv2 import cv2
import sys
import numpy as np
import keyboard 

TAG_TYPE = "DICT_ARUCO_ORIGINAL"
WINDOW_SIZE = 1000
W = 1000
H = 750
LINE = 2 * (H//3)
TIME = 5
currrent_time = 0

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

# verify that the supplied ArUCo tag exists and is supported by OpenCV
if ARUCO_DICT.get(TAG_TYPE, None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
        TAG_TYPE))
    sys.exit(0)
# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(TAG_TYPE))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[TAG_TYPE])
arucoParams = cv2.aruco.DetectorParameters_create()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    timeCheck = time.time()

    frame = vs.read()
    frame = imutils.resize(frame, width =WINDOW_SIZE)


    
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters = arucoParams)    
    cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))
    frame = cv2.flip(frame, 1) 
   
    
    if len(corners) > 0:
        frame = cv2.flip(frame, 1) 
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            frame = cv2.flip(frame, 1) 
   
            if cY < LINE:
                cv2.putText(frame, "Scan", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "Enter" + str(current_time), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                current_time += time.time()
            
            if current_time > TIME:
                keyboard.press_and_release("enter")
                current_time = 0

    cv2.namedWindow('Frame', cv2.WINDOW_AUTOSIZE)
    #cv2.rectangle(frame, (W // 4, H // 4), ((W // 4) * 3, (H // 4) * 3), (0, 0, 255), 3)
    cv2.line(frame, (0, LINE), (W, LINE), (0,255,0),2)
    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    print('fps - ',1/(time.time()-timeCheck))


cv2.destroyAllWindows()
vs.stop()