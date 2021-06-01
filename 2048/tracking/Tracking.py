import vars.config as cfg
import vars.constants as c
import cv2
import imutils
import numpy as np
import keyboard
import time
from imutils.video import VideoStream

def press(input, key='a'):
    if input and not cfg.last_input:
        keyboard.press_and_release(key)
        cfg.cooldown = 50
    cfg.last_input = input

# EDIT
# function to detect Aruco with OpenCV

def auto_range():
    initialBoundingBox = None
    vs = VideoStream(src=0).start()
    time.sleep(1.0)

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width = c.WIN_SIZE)

        #display frame
        frame = cv2.flip(frame, 1)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            initialBoundingBox = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
            # crop original frame
            roi = frame[int(initialBoundingBox[1]):int(initialBoundingBox[1]+initialBoundingBox[3]), 
            int(initialBoundingBox[0]):int(initialBoundingBox[0]+initialBoundingBox[2])]

            # convert to hsv
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)        

            # get a height and width
            (height, width, channels) = roi.shape

            hue = []
            sat = []
            val = []

            #parse hsv values
            for y in range(height):
                for x in range(width):
                    (h,s,v) = hsv[y,x]
                    hue.append(h)
                    sat.append(s)
                    val.append(v)
            
            # determine max
            hMaxValue = max(hue, key = hue.count)
            sMaxValue = max(sat, key = sat.count)
            vMaxValue = max(val, key = val.count)

            # calculate upper/lower bounds
            upperBound = (int(hMaxValue + c.PLUS_MINUS), int(sMaxValue + 2*c.PLUS_MINUS), int(vMaxValue + 3*c.PLUS_MINUS))
            lowerBound = (int(hMaxValue - c.PLUS_MINUS), int(sMaxValue - 2*c.PLUS_MINUS), int(vMaxValue - 3*c.PLUS_MINUS))
            
            print("BOUNDS:", lowerBound,"  ", upperBound)

            vs.stop()
            cv2.destroyAllWindows()
            return lowerBound, upperBound            


def detect_color(img, points):
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #     if cfg.cooldown > 0:
    #         print(cfg.cooldown)

    # resize the img, blur it, and convert it to the HSV
    # color space
    img = imutils.resize(img, width=600)
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask

    mask = cv2.inRange(hsv, cfg.colorLower, cfg.colorUpper)
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
        centroid = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(centroid)
        M = cv2.moments(centroid)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the img,
            # then update the list of tracked points
            #cv2.circle(img, (int(x), int(y)), int(radius),
            #           (0, 255, 255), 2)
            #cv2.circle(img, center, 5, (0, 0, 255), -1)
            pass
    # update the points queue
    cfg.pts.appendleft(center)

    checkKeyPress()

    drawLine(img)

    img = cv2.flip(img, 1)
    return img

def checkKeyPress():
    if((len(cfg.pts) == c.maxlen) and cfg.pts[(c.maxlen) - 1] is not None and cfg.pts[0] is not None):
        xdif = cfg.pts[c.maxlen-1][0] - cfg.pts[0][0]
        ydif = cfg.pts[c.maxlen-1][1] - cfg.pts[0][1]

        if xdif > cfg.threshold:
            press(True, key='d')
        elif xdif < -1 * cfg.threshold:
            press(True, key='a')
        elif ydif > cfg.threshold:
            press(True, key='w')
        elif ydif < -1 * cfg.threshold:
            press(True, key='s')
        else:
            press(False)


def drawLine(img):
    # loop over the set of tracked points
    for i in range(1, len(cfg.pts)):
        # if either of the tracked points are None, ignore
        # them
        if cfg.pts[i - 1] is None or cfg.pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(c.LINE_THICKNESS / float(i + 1)) * 2.5)
        if cfg.last_input or cfg.cooldown > 0:
            cv2.line(img, cfg.pts[i - 1], cfg.pts[i], c.LINE_GREEN, thickness)
            if cfg.cooldown > 0:
                cfg.cooldown -= 1
        else:
            cv2.line(img, cfg.pts[i - 1], cfg.pts[i], c.LINE_RED, thickness)
    return img


def detect_aruco(img, points):
    global up_frames, down_frames, left_frames, right_frames

    arucoDict = cv2.aruco.Dictionary_get(c.ARUCO_DICT[c.TAG_TYPE])
    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    cv2.aruco.drawDetectedMarkers(img, corners, ids, (0, 255, 0))

    if len(corners) > 0:
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            # compute and draw the center (x, y)-coordinates of the ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            center = (cX, cY)

        cfg.pts.appendleft(center)

    checkKeyPress()

    drawLine(img)

    img = cv2.flip(img, 1)
    return img
