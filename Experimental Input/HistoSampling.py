import cv2
import imutils
from imutils.video import VideoStream
import time

WINDOW_SIZE = 1000
RANGE = 4

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
        r = initialBoundingBox
        img_roi = frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])] 
        #cv2.imshow("imageHSV",img_roi)

        hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        # hue = [entry[0] for entry in hsv]
        # print(list(hue))

        hue = []
        sat = []
        val = []
        # for entry in hsv:
        #     hue.append(hsv[entry][0])
        #     sat.append(hsv[entry][1])
        #     val.append(hsv[entry][2])

        for row in hsv:
            for col in row:
                hue.append(col[0])
                sat.append(col[1])  
                val.append(col[2])
                
        # hueMaxCount = max(hue,key=hue.count)
        # satMaxCount = max(sat, key=sat.count)
        # valMaxCount = max(val, key=val.count)
        
        # upperBound = (hueMaxCount + RANGE, satMaxCount + RANGE, valMaxCount + RANGE)
        # lowerBound = (hueMaxCount - RANGE, satMaxCount - RANGE, valMaxCount - RANGE)

        # print(upperBound, "  ", lowerBound)
    frame = cv2.flip(frame, 1)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initialBoundingBox = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
        print(initialBoundingBox)
        frame = cv2.rectangle(frame,initialBoundingBox[0:2], initialBoundingBox[2:4], (255, 0, 0), 2)
        cv2.imshow("asdf", frame)
        time.sleep(10)
        break
        print(initialBoundingBox)
    elif key == 27:
        break

vs.stop()
cv2.destroyAllWindows()