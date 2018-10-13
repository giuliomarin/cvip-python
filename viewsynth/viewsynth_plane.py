from cvip import dataio
from calibration import utils
from cvip import xmlparser as xml
from cvip import transformations as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Parameters
img_path = '/Users/giulio/git/build/Nitrogen/bin/Debug/charucoboard0_res6x7_dpi254_4.png'
calib_path = '/Users/giulio/Desktop/6/ctgm020_sir.yml'
image_size = (180, 160)  # (height, width) mm
R_cam = tf.rotation_matrix(np.deg2rad(180), [1, 0, 0])[:3, :3]
T_cam = np.asarray([-80, 90, 300]).reshape(3, 1)
# R_cam = np.asarray([[9.9633572699294704e-01, 5.0380579550958884e-02, 6.9115239430577458e-02], [7.6961630513651805e-02, -8.8062059293854134e-01, -4.6752997628093551e-01], [3.7309871965964789e-02 ,4.7113604032877965e-01 ,    -8.8127113021884584e-01]])
# T_cam = np.asarray([-1.1257096127255562e+02, 9.6974428146112345e+01, 3.5490264682616044e+02]).reshape(3, 1)

# # R_cam = xml.get(xml.parse('/Data/13_calibration/charuco/orig/homography0.xml'), ['RT'])[:3, :3]
# # T_cam = xml.get(xml.parse('/Data/13_calibration/charuco/orig/homography0.xml'), ['RT'])[:3, 3].reshape(3, 1)
# RT_cam = utils.createRT(R_cam, T_cam)
# p = '/Data/13_calibration/charuco_detection/0deg/2mark/ch5/homography0.xml'
# R_s = xml.get(xml.parse(p), ['RT'])[:3, :3]
# T_s = xml.get(xml.parse(p), ['RT'])[:3, 3].reshape(3, 1)
# RT_s = utils.createRT(R_s, T_s)
# RT_diff = utils.invRT(RT_s).dot(RT_cam)
# RR = np.eye(4, 4)
# RR[:3, :3] = RT_diff[:3, :3]
# print '%.2f deg' % abs(np.rad2deg(tf.rotation_from_matrix(RR)[0]))
# print '%.2f mm' % np.linalg.norm(RT_diff[:3, 3])
# exit(0)

# Load image
img, flag = dataio.imread(img_path)
cm = 'gray' if flag == 0 else None
kernel = np.ones((7, 7), np.float32) / 49
img = cv2.filter2D(img, -1, kernel)
# plt.figure('Image plane')
# plt.imshow(img, cmap=cm)
# plt.show()

# Load camera calibration
calib = utils.SensorCalib(calib_path)
K = calib.camera_calib[0].K
# Project image into image plane
range_r_px = np.arange(img.shape[0])
range_c_px = np.arange(img.shape[1])
range_r_mm = (range_r_px + 1) / float(img.shape[0]) * float(image_size[0])
range_c_mm = (range_c_px + 1) / float(img.shape[1]) * float(image_size[1])
img_cam = np.ones(calib.camera_calib[0].resolution[::-1], img.dtype) * 255
for r, r_mm in zip(range_r_px, range_r_mm):
    if r % 100 == 0:
        print r
    for c, c_mm in zip(range_c_px, range_c_mm):
        color = img[(img.shape[0] - 1) - r, c]
        # print "r=[%d, %.1f] c=[%d, %.1f] color: %d" % (r, r_mm, c, c_mm, color)
        xyz = np.asarray([c_mm, r_mm, 0.]).reshape(3, 1)
        uvz = K.dot(R_cam.dot(xyz) + T_cam)
        uv_f = uvz[:2] / uvz[2]
        uv = uv_f.astype(int)
        if (0 <= uv[0] < img_cam.shape[1]) and (0 <= uv[1] < img_cam.shape[0]):
            img_cam[uv[1], uv[0]] = color

dataio.imwrite('/Users/giulio/Desktop/6/synth_4.png', img_cam)
# plt.figure('Image camera')
# plt.imshow(img_cam, cmap=cm)
# plt.show()