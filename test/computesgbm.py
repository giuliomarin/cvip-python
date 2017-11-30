import cv2
from cvip import dataio
from matplotlib import pyplot as plt
import numpy as np
import sys

# s = sys.argv[1]
# s = '4'
# img1 = cv2.cvtColor(dataio.imread('/Users/giulio/Desktop/stereo/rect/%s_l.png' % s)[0], cv2.COLOR_BGR2GRAY)
# img2 = cv2.cvtColor(dataio.imread('/Users/giulio/Desktop/stereo/rect/%s_r.png' % s)[0], cv2.COLOR_BGR2GRAY)

img1 = dataio.imread('/Data/0_Dataset/multicam_out/10/img_r10_s3_c1_rect.png')[0]
img2 = dataio.imread('/Data/0_Dataset/multicam_out/10/img_r10_s3_c2_rect.png')[0]

window_size = 11
mDisp = 0

if False:
    stereo = cv2.StereoSGBM_create(minDisparity = mDisp,
                                   numDisparities = 64,
                                   blockSize = 13,
                                   P1 = 8 * 3 * window_size ** 2,
                                   P2 = 32 * 3 * window_size ** 2,
                                  disp12MaxDiff = 16,
                                  preFilterCap = 31,
                                  uniquenessRatio = 10,
                                  speckleWindowSize = 100,
                                  speckleRange = 32,
                                  mode = 0)
else:
    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=13)
#
# window_size = 5
# stereo = cv2.StereoSGBM_create(minDisparity = 180,
#                                numDisparities = 128,
#                                blockSize = 15,
#                                P1 = 8 * 3 * window_size ** 2,
#                                P2 = 32 * 3 * window_size ** 2,
#                               disp12MaxDiff = 1,
#                               preFilterCap = 63,
#                               uniquenessRatio = 1,
#                               speckleWindowSize = 0,
#                               speckleRange = 1,
#                               mode = 1)


disparity = stereo.compute(img1, img2).astype(np.float32) / 16.
# depth = 1.74659325e+05 / disparity
# depth[disparity <= mDisp] = 0
# dataio.imwrite32f('/Users/giulio/Desktop/stereo/%s.png' % s, depth)
plt.imshow(disparity)
plt.colorbar()
plt.show()