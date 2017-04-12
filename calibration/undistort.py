import numpy as np
import cv2
from cvip import ymlparser, utils, xmlparser
import sys

#########################
# Parameters
#########################

c = 0
imgPath = '/Data/3_calibration/30_Q_50C_00078/master_3.png'
calibPath = sys.argv[1] #'/GitHub/build/Nitrogen/bin/Debug/calib.xml'
# calibPath = '/Volumes/RegressionTesting/SIR/RailTests/genericTests/AQP_Scanner/Calibration/01_27_2017/30_Q_50C_00078/Calib_30_Q_50C_00078.xml'

##########################
# Load calibration
##########################

try:
    if True:
        calib = xmlparser.parse(calibPath)
        cam = 'camera_%d' % c
        K = xmlparser.getmat(calib, ['camera_calibrations', cam, 'K'])
        D = xmlparser.getmat(calib, ['camera_calibrations', cam, 'D'])
        R = xmlparser.getmat(calib, ['camera_calibrations', cam, 'R'])
        T = xmlparser.getmat(calib, ['camera_calibrations', cam, 'T'])
    if False:
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
mapx, mapy = cv2.initUndistortRectifyMap(K, D, None, K, (w, h), 5)
imgund = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# cv2.imwrite(imgfilebase % 'imgund.png', imgund)
cv2.imwrite('und.png', imgund)
bothimg = utils.resizeimgw(np.hstack((img, imgund)), 1024)
cv2.imshow('original & undistorted', bothimg)
cv2.waitKey(0)

