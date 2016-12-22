import numpy as np
import cv2
import sys
from random import uniform, randrange
from cvip import utils, ymlparser, dataio

sys.path.append('/GitHub/cvip/python')

#########################
# Parameters
#########################

calibPath = r'/Users/giulio/Desktop/collection_20161002/out/calib_all.yml'
s = 2
imgpath1 = '/Users/giulio/Desktop/collection_20161002/out/calib2/%d/img_r1_s1_1.png' % s
imgpath2 = '/Users/giulio/Desktop/collection_20161002/out/calib2/%d/img_r1_s1_2.png' % s

N_CHECKERS = (10, 8)  # (points_per_row,points_per_colum)
SIZE_CHECKERS = 20.0  # mm

# Visualization
H_IMGS = 400  # -1 for original size

#########################
# Functions
#########################

def getoptimalimg(img):
    img = np.sqrt(img)
    img /= max(img.flatten())
    img *= 255.0
    return img.astype(np.uint8)

def getimage(imgpath):
    print 'Image: %s' % imgpath,
    # load image and convert to grayscale
    img, isfloat = dataio.imread(imgpath)
    if isfloat:
        gray = getoptimalimg(img)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    else:
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img, gray

##########################
# Calibration
##########################

calib = ymlparser.parse(calibPath)
c = 0
K_l = calib['camera_calibrations']['camera_%d' % c]['K']
D_l = calib['camera_calibrations']['camera_%d' % c]['D']
R_l = calib['camera_calibrations']['camera_%d' % c]['R']
T_l = calib['camera_calibrations']['camera_%d' % c]['T']
res_l = calib['camera_calibrations']['camera_%d' % c]['resolution']

c = 1
K_r = calib['camera_calibrations']['camera_%d' % c]['K']
D_r = calib['camera_calibrations']['camera_%d' % c]['D']
R_r = calib['camera_calibrations']['camera_%d' % c]['R']
T_r = calib['camera_calibrations']['camera_%d' % c]['T']
res_r = calib['camera_calibrations']['camera_%d' % c]['resolution']

# Compute relative transformation
R = R_r.dot(np.linalg.inv(R_l))
T = -R_r.dot(np.linalg.inv(R_l).dot(T_l)) + T_r

# Rectification
newsize = tuple(res_l)
R_l, R_r, P_l, P_r, _, _, _ = cv2.stereoRectify(K_l, D_l, K_r, D_r, newsize, R, T, flags = cv2.CALIB_ZERO_DISPARITY, alpha = 0)

rectMap = [[[], []], [[], []]]
rectMap[0][0], rectMap[0][1] = cv2.initUndistortRectifyMap(K_l, D_l, R_l, P_l, newsize, cv2.CV_16SC2)
rectMap[1][0], rectMap[1][1] = cv2.initUndistortRectifyMap(K_r, D_r, R_r, P_r, newsize, cv2.CV_16SC2)

img_l, gray_l = getimage(imgpath1)
img_r, gray_r = getimage(imgpath2)

imgorig_l = utils.resizeimgh(img_l, H_IMGS)
imgorig_r = utils.resizeimgh(img_r, H_IMGS)
imgorig = np.hstack((imgorig_l, imgorig_r))

imgRect_l = cv2.remap(img_l, rectMap[0][0], rectMap[0][1], cv2.INTER_CUBIC)
imgRect_r = cv2.remap(img_r, rectMap[1][0], rectMap[1][1], cv2.INTER_CUBIC)

imgtoshow_l = utils.resizeimgh(imgRect_l, H_IMGS)
imgtoshow_r = utils.resizeimgh(imgRect_r, H_IMGS)
imgtoshow = np.hstack((imgtoshow_l, imgtoshow_r))

lines = [((0, int(r)), (imgtoshow.shape[1], int(r)), (uniform(0, 255), uniform(0, 255), uniform(0, 255))) for r in np.linspace(0, imgtoshow.shape[0], 20)]
for pt in lines:
    cv2.line(imgtoshow, pt[0], pt[1], pt[2], 1)

# imgtoshow = np.vstack((imgorig, imgtoshow))

# cv2.imwrite(imgfilebase % 'rectimg2_1.png', imgRect_l)
# cv2.imwrite(imgfilebase % 'rectimg1_1.png', imgRect_r)
# cv2.imwrite('rect.png', imgtoshow)
cv2.imshow('orig', imgorig)
cv2.imshow('rect', imgtoshow)
cv2.waitKey(0)