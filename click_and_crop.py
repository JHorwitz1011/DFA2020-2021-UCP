import argparse
import cv2
import numpy as np

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
selected = False

# create a blank 300x300 image for the current hovered color
canvas = np.zeros((300, 300, 3), np.uint8)

# reference image
image = cv2.imread("blob.jpg")
color = (0,0,0)
def display_color(event, x, y, flags, param):
	global selected
	if not selected:
		print("selected color is: " + str(image[y,x]))
		canvas[:] = image[y,x]
	# # check to see if the left mouse button was released
	if event == cv2.EVENT_LBUTTONUP:
		# grab the color from the (x,y) coordinate
		print("final selected color is: " + str(image[y,x]))
		selected = True
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", display_color)
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	cv2.imshow("selected color", canvas)

	# wait until user exits
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, break from the loop
	if key == ord("q"):
		break
# if there are two reference points, then crop the region of interest
# from teh image and display it

# close all open windows
cv2.destroyAllWindows()