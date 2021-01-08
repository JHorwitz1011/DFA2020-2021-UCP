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
	# grab global variable so it can be referenced
	global selected

	if not selected:
		print("selected color is: " + str(image[y,x]))
		canvas[:] = image[y,x]
	# check to see if the left mouse button was released
		if event == cv2.EVENT_LBUTTONUP:
			# grab the color from the (x,y) coordinate
			print("final selected color is: " + str(image[y,x]))
			selected = True

# initialize window so we can put an callback on it
cv2.namedWindow("image")

# assigns display_color function to call after any mouse action
cv2.setMouseCallback("image", display_color)



# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("selected color", canvas)

	# wait until user exits
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, break from the loop
	if key == ord("q"):
		break
# close all open windows
cv2.destroyAllWindows()