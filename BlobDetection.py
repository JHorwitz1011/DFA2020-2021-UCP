# 1 detect blobs
# 2 have user click on blob to use
# 3 determine color of blob
# 4 using unique color chosen, track blob using color
#
#

# Standard imports
import cv2
import numpy as np;

# Read image
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#ret, im = camera.read()
im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)
cv2.imshow("original image", im)
cv2.waitKey(0)
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()

# Detect blobs.
keypoints = detector.detect(im)

cartisean_points = cv2.KeyPoint_convert(keypoints)
print(cartisean_points)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

print("got to show")
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)