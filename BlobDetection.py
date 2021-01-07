# 1 take picture, get BGR and HSV model
# 2 have user select color of object
# 3 get a black and white mask based on selected color
# 4 blob detection on mask
# 5 get keypoints from mask, and determine closest blob to original selection

# Standard imports
import cv2
import numpy as np

############################# 1 #######################################

#starting "picture"
print("take picture of tracker in visible light")
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
	ret, bgr = camera.read()
	cv2.imshow("Arrange Tracker", bgr)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, break from the loop
	if key == ord("q"):
		break
cv2.destroyWindow("Arrange Tracker")

#convert to hsv color scheme for masking
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

#show bgr and hsv images
cv2.imshow("BGR image", bgr)
cv2.waitKey(0)

cv2.imshow("HSV image", hsv)
cv2.waitKey(0)
cv2.destroyWindow("HSV image")


############################## 2 ########################################

# prompt user to select a color
print("please select your tracker (for color recognition)") # WIP will most likely be some other thing on the GUI

#variable to determine if color has been selected already
selected = False
selected_color = (0,0,0)
canvas = np.zeros((300, 300, 3), np.uint8)

# callback method
def select_color(event, x, y, flags, param):
	# grab global variable so it can be referenced
	global selected, selected_color

	if not selected:
		print("selected color in HSV is: " + str(hsv[y,x]))
		canvas[:] = bgr[y,x]
	# check to see if the left mouse button was released
		if event == cv2.EVENT_LBUTTONUP:
			# grab the color from the (x,y) coordinate
			print("final selected color in HSV is: " + str(hsv[y,x]))
			selected = True
			selected_color = hsv[y,x]

# put action listener on mouse listener
cv2.setMouseCallback("BGR image", select_color)

while not selected:
	# wait until user exits
	cv2.imshow("canvas", canvas)
	key = cv2.waitKey(1) & 0xFF
		# if the 'q' key is pressed, break from the loop
	if key == ord("q"):
		break
################################ 3 #####################################
print("selected color = " + str(selected_color))
diff = [i * 0.1 for i in selected_color]

print("diff = " + str(diff))
lower_bound = [r - l for l, r, in zip(diff[:-1], selected_color[:-1])]
lower_bound.append(0)
upper_bound = [r + l for l, r, in zip(diff[:-1], selected_color[:-1])]
upper_bound.append(255)
lower_bound = tuple(lower_bound)
upper_bound = tuple(upper_bound)
print("upper bound is:"  + str(upper_bound))
print("lower bound is:" + str(lower_bound))
mask = cv2.inRange(hsv, lower_bound, upper_bound)
cv2.imshow("mask", mask)
cv2.waitKey(0)
result = cv2.bitwise_and(bgr, bgr, mask = mask) 
cv2.imshow("filter?", result)
cv2.waitKey(0)



##########################################

################################## 4 ###########################

inverted = cv2.bitwise_not(mask)
detector = cv2.SimpleBlobDetector_create()

# Detect blobs.
keypoints = detector.detect(inverted)

cartisean_points = cv2.KeyPoint_convert(keypoints)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(result, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

print("got to show, keypoints at: " + str(cartisean_points))
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

############################# end ##################################
cv2.destroyAllWindows()

print("ending")

