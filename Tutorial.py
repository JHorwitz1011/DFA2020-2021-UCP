# How to open and read video streams


import numpy as np
import imutils
from cv2 import cv2 as cv
from collections import deque

# Setup
FRAME_WIDTH = 800
FRAME_HEIGHT = 800
MAXBUFFER = 64

colorLower = (0, 200, 200)  # (29,86,6)
colorUpper = (10, 255, 255)  # (64,255,255)
pts = deque(maxlen=MAXBUFFER)

# cv.namedWindow('WebcamTest')

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not camera.isOpened():
    print("Camera could not be referenced")
    exit(0)


while True:
    ret, frame = camera.read()

    if ret:
        # cv.imshow('frame',frame)

        # Process frame @ lower quality level
        frame = imutils.resize(frame, width=600)
        blurred = cv.GaussianBlur(frame, (11, 11), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv, colorLower, colorUpper)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        cv.imshow('Mask', mask)

        # Pull contours to draw
        contours = cv.findContours(
            mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None

        if len(contours) > 0:
            maxC = max(contours, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(maxC)
            M = cv.moments(maxC)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv.circle(frame, (int(x), int(y)),
                          int(radius), (0, 255, 255), 2)
                cv.circle(frame, center, 5, (0, 0, 255), -1)

        pts.appendleft(center)

        # display trail
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue

            thickness = int(np.sqrt(MAXBUFFER / float(i+1)) * 2.5)
            cv.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)

        frame = cv.flip(frame, 1)
        cv.imshow('Frame', frame)

        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
        #print('fps - ', 1/(time.time()-timeCheck))

    else:
        break

cv.destroyAllWindows()
camera.release()
