import cv2
from cvip import dataio
from matplotlib import pyplot as plt
import numpy as np
import sys

s = sys.argv[1]
# s = '4'
img1 = cv2.cvtColor(dataio.imread('/Users/giulio/Desktop/stereo/rect/%s_l.png' % s)[0], cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(dataio.imread('/Users/giulio/Desktop/stereo/rect/%s_r.png' % s)[0], cv2.COLOR_BGR2GRAY)

window_size = 5
mDisp = 140
stereo = cv2.StereoSGBM_create(minDisparity = mDisp,
                               numDisparities = 176,
                               blockSize = 13,
                               P1 = 8 * 3 * window_size ** 2,
                               P2 = 32 * 3 * window_size ** 2,
                              disp12MaxDiff = 16,
                              preFilterCap = 31,
                              uniquenessRatio = 10,
                              speckleWindowSize = 100,
                              speckleRange = 32,
                              mode = 0)
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


disparity = stereo.compute(img1, img2).astype(np.float32) / 16.0
depth = 1.74659325e+05 / disparity
depth[disparity <= mDisp] = 0
dataio.imwrite32f('/Users/giulio/Desktop/stereo/%s.png' % s, depth)
# plt.imshow(depth)
# plt.colorbar()
# plt.show()