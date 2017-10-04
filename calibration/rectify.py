import numpy as np
import cv2
import sys
from random import uniform, randrange
from cvip import utils, ymlparser, xmlparser, dataio
from matplotlib import pyplot as plt

sys.path.append('/GitHub/cvip/python')

#########################
# Parameters
#########################

# calibPath = r'/Users/giulio/Downloads/calib2cameraRect.xml'
# calibPath = r'/Users/giulio/Downloads/calib445.xml'
calibPath = '/Volumes/AlgoShared/giulio/Snapshot1/sir/CalibrationFile/ctgm020.xml'
s = 1
cameras = ['master', 'slave', 'color0']
c1 = 0
c2 = 1
imgpath = '/Users/giulio/Desktop/out/%s_1.png'
# imgpath1 = imgpath % cameras[c1]
# imgpath2 = imgpath % cameras[c2]
imgpath1 = '/Volumes/AlgoShared/giulio/Snapshot1/sir/Frames/master_1.png'
imgpath2 = '/Volumes/AlgoShared/giulio/Snapshot1/sir/Frames/slave_1.png'

N_CHECKERS = (10, 8)  # (points_per_row,points_per_colum)
SIZE_CHECKERS = 20.0  # mm

# Visualization
H_IMGS = 600  # -1 for original size

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
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    else:
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = dataio.opencv2matplotlib(img)
    return img, gray

##########################
# Calibration
##########################

if calibPath.endswith('xml'):
    calib = xmlparser.parse(calibPath)
    cam = 'camera_%d' % c1
    K_l = xmlparser.get(calib, ['camera_calibrations', cam, 'K'])
    D_l = xmlparser.get(calib, ['camera_calibrations', cam, 'D'])
    R_l = xmlparser.get(calib, ['camera_calibrations', cam, 'R'])
    T_l = xmlparser.get(calib, ['camera_calibrations', cam, 'T'])
    res_l = xmlparser.get(calib, ['camera_calibrations', cam, 'resolution']).strip().split()
    res_l[0] = int(res_l[0])
    res_l[1] = int(res_l[1])
    cam = 'camera_%d' % c2
    K_r = xmlparser.get(calib, ['camera_calibrations', cam, 'K'])
    D_r = xmlparser.get(calib, ['camera_calibrations', cam, 'D'])
    R_r = xmlparser.get(calib, ['camera_calibrations', cam, 'R'])
    T_r = xmlparser.get(calib, ['camera_calibrations', cam, 'T'])
    res_r = xmlparser.get(calib, ['camera_calibrations', cam, 'resolution']).strip().split()
    res_r[0] = int(res_r[0])
    res_r[1] = int(res_r[1])

else:
    calib = ymlparser.parse(calibPath)
    K_l = calib['camera_calibrations']['camera_%d' % c1]['K']
    D_l = calib['camera_calibrations']['camera_%d' % c1]['D']
    R_l = calib['camera_calibrations']['camera_%d' % c1]['R']
    T_l = calib['camera_calibrations']['camera_%d' % c1]['T']
    res_l = calib['camera_calibrations']['camera_%d' % c1]['resolution']

    K_r = calib['camera_calibrations']['camera_%d' % c2]['K']
    D_r = calib['camera_calibrations']['camera_%d' % c2]['D']
    R_r = calib['camera_calibrations']['camera_%d' % c2]['R']
    T_r = calib['camera_calibrations']['camera_%d' % c2]['T']
    res_r = calib['camera_calibrations']['camera_%d' % c2]['resolution']

# Compute relative transformation
R = R_r.dot(np.linalg.inv(R_l))
T = -R_r.dot(np.linalg.inv(R_l).dot(T_l)) + T_r

# Rectification
newsize = tuple(res_l)
R_l, R_r, P_l, P_r, _, _, _ = cv2.stereoRectify(K_l, D_l, K_r, D_r, newsize, R, T, flags = cv2.CALIB_ZERO_DISPARITY, alpha = 0)

print R_l
print
print P_l
print P_r

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

# imgpathout = '/Users/giulio/Desktop/stereo/%s.png'
# dataio.imwrite(imgpathout % ('%d_l' % s), imgRect_l)
# dataio.imwrite(imgpathout % ('%d_r' % s), imgRect_r)
# cv2.imwrite('rect.png', imgtoshow)
# cv2.imshow('orig', imgorig)
# cv2.imshow('rect', imgtoshow)
plt.imshow(imgtoshow)
plt._show()
# cv2.waitKey(0)