import cv2
from cvip import utils, dataio
from moviepy.editor import *

# Read the images to be aligned
im1 = cv2.imread("/Users/giulio/Desktop/old.jpg")
im2 = cv2.imread("/Users/giulio/Desktop/new.jpg")

# align 2 to 1
im2_a = utils.alignimage(im1, im2)

# crop images
tl = (0, 0)
br = (738, 1000)

im1_crop = utils.cropimage(im1, (tl, br))
im2_a_crop = utils.cropimage(im2_a, (tl, br))

# Save images
cv2.imwrite("/Users/giulio/Desktop/1.jpg", im1_crop)
cv2.imwrite("/Users/giulio/Desktop/2.jpg", im2_a_crop)

# create gif
clip = ImageSequenceClip([dataio.opencv2matplotlib(im1_crop), dataio.opencv2matplotlib(im2_a_crop)], fps = 2)
# clip = clip.resize(1.0 / 5.0)
clip.write_gif('/Users/giulio/Desktop/gif.gif')
