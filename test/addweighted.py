import cv2
import numpy as np

a = 0.5
b = 0.5
g = 0

# Read the images to be aligned
im1 = cv2.imread("/Users/giulio/Desktop/old.jpg")
im2 = cv2.imread("/Users/giulio/Desktop/new_a.jpg")

im = cv2.addWeighted(im1, a, im2, b, g)

cv2.imwrite("/Users/giulio/Desktop/comb.jpg", im)
