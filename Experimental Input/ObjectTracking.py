import imutils
from imutils.video import VideoStream
from cv2 import cv2
import time

TRACKERTYPE = "kcf"
WINDOW_SIZE = 1000

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
        (success, box) = tracker.update(frame)
        if success:
            (x,y,w,h) = [int(v) for v in box]
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
            
        #frame = cv2.flip(frame, 1)

        info = [("Tracker", TRACKERTYPE), ("Success", "Yes" if success else "No"), ("FPS", "{:.2f}".format(1/(time.time()-timeCheck))),]
        
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initialBoundingBox = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
        tracker.init(frame, initialBoundingBox)
    elif key == 27:
        break

vs.stop()
cv2.destroyAllWindows()
