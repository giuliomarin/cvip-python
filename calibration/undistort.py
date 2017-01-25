import numpy as np
import cv2
from cvip import ymlparser, utils
import sys

#########################
# Parameters
#########################

c = 3
imgPath = '/Users/giulio/Desktop/collection_20161002/out/calib2/1/img_r1_s2_4.png'
calibPath = '/Users/giulio/Desktop/collection_20161002/out/calib_all.yml'

##########################
# Load calibration
##########################

try:
    if True:
        calib = ymlparser.parse(calibPath)
        cam = calib['camera_calibrations']['camera_%d' % c]
        K = cam['K']
        D = cam['D']
        R = cam['R']
        T = cam['T']
    if False:
        with open(calibPath % 'calib.txt', 'r') as calibfile:
            # K
            K = []
            calibstr = calibfile.readline()
            K = np.append(K, [float(x) for x in calibfile.readline().split()])
            K = np.append(K, [float(x) for x in calibfile.readline().split()])
            K = np.append(K, [float(x) for x in calibfile.readline().split()])
            K = K.reshape(3, 3)

            # D
            D = []
            calibstr = calibfile.readline()
            calibstr = calibfile.readline()
            D = np.append(D, [float(x) for x in calibfile.readline().split()])
except:
    sys.exit('Unable to parse calibration file')

##########################
# Undistortion
##########################

print '\nTest undistortion'
img = cv2.imread(imgPath)
h, w = img.shape[:2]
Knew, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
# print 'Knew:\n%s' % utils.tostr(Knew)
mapx, mapy = cv2.initUndistortRectifyMap(K, D, None, Knew, (img.shape[1], img.shape[0]), 5)
imgund = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# cv2.imwrite(imgfilebase % 'imgund.png', imgund)
bothimg = utils.resizeimgw(np.hstack((img, imgund)), 1024)
cv2.imshow('original & undistorted', bothimg)
cv2.waitKey(0)

