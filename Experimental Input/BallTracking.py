# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math
import keyboard
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# orangeLower = (0, 220, 158)
# orangeUpper = (12, 255, 255)
orangeLower = (0, 130, 130)
orangeUpper = (19, 255, 255)   
   
###constants###   
maxlen=10   
threshold = 150 
LINE_RED = (0, 0, 255)
LINE_GREEN = (0, 255, 0) 

##vraiables##
cooldown = 0
pts = deque(maxlen=maxlen)   
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

last_input = False
def press(input, key='a'):
	global cooldown
	global last_input
	if input and not last_input:
		keyboard.press_and_release(key)
		cooldown = 50
	last_input = input

# keep looping
while True:
	if cooldown > 0:
		print(cooldown)
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, orangeLower, orangeUpper)
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
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
					   (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# update the points queue
	pts.appendleft(center)

	if(len(pts) == maxlen and pts[maxlen-1] is not None and pts[0] is not None):
		#print('left:', pts[0])
		#print('right:', pts[maxlen-1])
		xdif = pts[maxlen-1][0] - pts[0][0]
		#print('xdif:', xdif)
		ydif = pts[maxlen-1][1] - pts[0][1]
		#print('ydif:', ydif)
		if xdif > threshold:
			print('RIGHT')
			press(True, key='d')
		elif xdif < -1 * threshold:
			print('LEFT')
			press(True, key='a')
		elif ydif > threshold:
			print('UP')
			press(True, key='w')
		elif ydif < -1 * threshold:
			print('DOWN')
			press(True, key='s')
		else:
			press(False)


    	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		if last_input or cooldown > 0:
			cv2.line(frame, pts[i - 1], pts[i], LINE_GREEN, thickness)
			if cooldown > 0:
				cooldown -= 1
		else:
			cv2.line(frame, pts[i - 1], pts[i], LINE_RED, thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()