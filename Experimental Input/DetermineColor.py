import imutils
from imutils.video import VideoStream
from cv2 import cv2
import time

TRACKERTYPE = "kcf"
WINDOW_SIZE = 1000
RANGE = 5

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

tracker = OPENCV_OBJECT_TRACKERS[TRACKERTYPE]()

initialBoundingBox = None

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(1.0)


while True:
    timeCheck = time.time()

    frame = vs.read()
    frame = imutils.resize(frame, width = WINDOW_SIZE)
    (H, W) = frame.shape[:2]

    if initialBoundingBox is not None:
        topLeft = (initialBoundingBox[2], initialBoundingBox[3])
        bottomRight = (initialBoundingBox[0], initialBoundingBox[1])

        
        roi = frame[int(initialBoundingBox[1]):int(initialBoundingBox[1]+initialBoundingBox[3]), 
                    int(initialBoundingBox[0]):int(initialBoundingBox[0]+initialBoundingBox[2])]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)        

        [height, width, channels] = roi.shape

        hue = []
        sat = []
        val = []

        for y in range(height):
            for x in range(width):
                [h,s,v] = hsv[y,x]
                hue.append(h)
                sat.append(s)
                val.append(v)
        
        hMaxValue = max(hue, key = hue.count)
        sMaxValue = max(sat, key = sat.count)
        vMaxValue = max(val, key = val.count)

        
        upperBound = (hMaxValue + RANGE, sMaxValue + RANGE, vMaxValue + RANGE)
        lowerBound = (hMaxValue - RANGE, sMaxValue - RANGE, vMaxValue - RANGE)

        print(lowerBound,"  ", upperBound)

        frame = cv2.rectangle(frame, initialBoundingBox, (255,0,0), 2 )
        
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initialBoundingBox = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
        tracker.init(frame, initialBoundingBox)
    elif key == 27:
        break

vs.stop()
cv2.destroyAllWindows()
