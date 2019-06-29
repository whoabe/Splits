import numpy as np
import cv2 as cv
 
img = cv.imread('receipt.jpg')
img = cv.rectangle(img, (230,457), (283,482), (0,255,0), 3)
 
# (230,457),(284,459),(283,482),(229,480)
# top left, top right, bottom right, bottom left

# Draw a Rectangle
# To draw a rectangle, the function is very similar and is called cv2.rectangle. Even this function accepts five input parameters:

# image object on which to draw
# coordinates of the vertex at the top left (x, y)
# coordinates of the lower right vertex (x, y)
# stroke color in BGR (not RGB, be careful)
# stroke thickness  (in pixels)

cv.imshow('image_with_rectangle',img)
cv.waitKey(0)