import os
from cvip import ymlparser, dataio
import utils
import utils
import numpy as np
import matplotlib.pyplot as plt
import cv2

"""
Detect checkerboard on reference camera and project it on all the other using calibration.
Undistort or rectify images depending on the calibration file.
"""

# Parameters
calib_path = '/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4_rect.yml'
# calib_path = '/Data/0_Dataset/multicam/bin/calib_out_s1c1_s2c2_40.yml'
imgsDir = '/Data/0_Dataset/multicam_out/0'
img_names = ['img_r10_s1_c1_rect.png', 'img_r10_s1_c2_rect.png', 'img_r10_s2_c1.png', 'img_r10_s2_c2.png', 'img_r10_s3_c1.png', 'img_r10_s3_c2.png', 'img_r10_s3_c3.png', 'img_r10_s4_c1_rect.png', 'img_r10_s4_c2_rect.png', 'img_r10_s4_c3.png']
# img_names = ['img_r10_s1_c1.png', 'img_r10_s2_c2.png']
refCam = 3

N_CHECKERS = (10, 8)  # (points_per_row, points_per_colum)
SIZE_CHECKERS = (0.02, 0.02)
# SIZE_CHECKERS = (20, 20)


def getImage(img_path):
    img, _ = dataio.imread(img_path)
    if len(img.shape) == 2:
        img = img.astype(np.float32) - np.min(img)
        img = img / np.max(img) * 255.0
        img = img.astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img


def figure_key_press(*args, **kwargs):
    def on_key_press(event):
        if event.key == 'escape':
            exit(0)
    fig = plt.figure(*args, **kwargs)
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    return fig

#######################
# Read calibration
#######################

calib = utils.SensorCalib(calib_path, 1)
if len(calib.camera_calib) != len(img_names):
    print 'Num cameras: %d but provided %d img_paths' % (len(calib.camera_calib), len(img_names))

#######################
# Find reference checkerboard
#######################

# Load image
img_path = os.path.join(imgsDir, img_names[refCam])
img = getImage(img_path)

# Get calibration camera
calib_cam = calib.camera_calib[refCam]
RT = utils.getExtrinsics(calib_cam)
K = utils.getIntrinsics(calib_cam)

# Undistort/Rectify image
imgund, rectify_flag = utils.undistortRectify(img, calib_cam)
gray = cv2.cvtColor(imgund, cv2.COLOR_RGB2GRAY)

# Find checkerboard
ret, corners = cv2.findChessboardCorners(gray, N_CHECKERS, None, flags=cv2.CALIB_CB_FILTER_QUADS + cv2.CALIB_CB_ADAPTIVE_THRESH)

# If not found return
if ret is not True:
    print 'Reference checkerboard not found'
    exit(1)

# refine image points using subpixel accuracy
cv2.cornerSubPix(gray, corners, (7, 7), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.001))

# Find the rotation and translation vectors.
objp = np.zeros((np.prod(N_CHECKERS), 3), np.float32)
objp[:, :2] = np.mgrid[0:N_CHECKERS[0] * SIZE_CHECKERS[0]:SIZE_CHECKERS[0], 0:N_CHECKERS[1] * SIZE_CHECKERS[1]:SIZE_CHECKERS[1]].T.reshape(-1, 2)

axis = np.float32([[SIZE_CHECKERS[0] * (N_CHECKERS[0] - 1), 0, 0], [0, SIZE_CHECKERS[0] * (N_CHECKERS[1] - 1), 0], [0, 0, -SIZE_CHECKERS[0] * (N_CHECKERS[0] - 1)]]).reshape(-1, 3)
_, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, K, None)
rmat, _ = cv2.Rodrigues(rvecs)

RTref = np.eye(4)
RTref[:3, :3] = rmat
RTref[:3, 3] = tvecs.transpose()
RTref = utils.invRT(RT).dot(RTref)

#######################
# Project reference checkerboard on all the cameras
#######################

for c in range(min(len(calib.camera_calib), len(img_names))):

    # Load image
    img_path = os.path.join(imgsDir, img_names[c])
    img = getImage(img_path)

    # Get calibration
    calib_cam = calib.camera_calib[c]
    RT = utils.getExtrinsics(calib_cam)
    K = utils.getIntrinsics(calib_cam)

    # Undistort/Rectify image
    imgund, rectify_flag = utils.undistortRectify(img, calib_cam)
    if rectify_flag:
        print 'Retify camera %d' % c
    else:
        print 'Undistort camera %d' % c
    gray = cv2.cvtColor(imgund, cv2.COLOR_RGB2GRAY)

    fig = figure_key_press('Camera %d - %s' % (c, img_names[c]))

    # Project reference checkerboard on this camera
    RTtot = RT.dot(RTref)
    Rtot = RTtot[:3, :3]
    Ttot = RTtot[:3, 3].reshape(3, 1)
    imgund = utils.drawCheckerboard(imgund, K, Rtot, Ttot, nx=N_CHECKERS[0], ny=N_CHECKERS[1], sx=SIZE_CHECKERS[0], sy=SIZE_CHECKERS[1])

    plt.imshow(imgund)
    # plt.imsave('/Data/0_Dataset/multicam/calib_characterization/%s' % img_names[c], imgund)
plt.show()

