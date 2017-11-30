import numpy as np
import cv2
import sys
import os
from random import uniform
import utils as utils_calib
from cvip import utils, ymlparser, xmlparser, dataio
from matplotlib import pyplot as plt

sys.path.append('/GitHub/cvip/python')


# def figure_key_press(*args, **kwargs):
#     def on_key_press(event):
#         if event.key == 'escape':
#             exit(0)
#     fig = plt.figure(*args, **kwargs)
#     fig.canvas.mpl_connect('key_press_event', on_key_press)
#     return fig


#########################
# Parameters
#########################

for s in range(11):

    calib_path = '/Data/0_Dataset/multicam_out/calib_s4.yml'
    c1 = 0
    c2 = 1

    imgpath1 = '/Data/0_Dataset/multicam_out/%d/img_r10_s4_c1.png' % s
    imgpath2 = '/Data/0_Dataset/multicam_out/%d/img_r10_s4_c2.png' % s

    N_CHECKERS = (10, 8)  # (points_per_row,points_per_colum)
    SIZE_CHECKERS = 20.0  # mm

    # Visualization
    W_IMGS = 600
    H_IMGS = 600  # -1 for original size

    #########################
    # Functions
    #########################

    # def getoptimalimg(img):
    #     img = np.sqrt(img)
    #     img /= max(img.flatten())
    #     img *= 255.0
    #     return img.astype(np.uint8)
    #
    # def getimage(imgpath):
    #     print 'Image: %s' % imgpath
    #     # load image and convert to grayscale
    #     img, isfloat = dataio.imread(imgpath)
    #     if isfloat:
    #         gray = getoptimalimg(img)
    #         img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    #     else:
    #         if len(img.shape) > 2:
    #             gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #         else:
    #             gray = img
    #             img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    #     return img, gray

    ##########################
    # Calibration
    ##########################

    calib = utils_calib.SensorCalib(calib_path)
    K1 = calib.camera_calib[c1].K
    D1 = calib.camera_calib[c1].D
    R1 = calib.camera_calib[c1].R
    T1 = calib.camera_calib[c1].T
    K2 = calib.camera_calib[c2].K
    D2 = calib.camera_calib[c2].D
    R2 = calib.camera_calib[c2].R
    T2 = calib.camera_calib[c2].T

    # Compute relative transformation
    R = R2.dot(np.linalg.inv(R1))
    T = -R2.dot(np.linalg.inv(R1).dot(T1)) + T2

    # Compute rectification
    newsize = tuple(calib.camera_calib[c1].resolution.astype(np.int))
    Rrect1, Rrect2, P1, P2, _, _, _ = cv2.stereoRectify(K1, D1, K2, D2, newsize, R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1)

    rectMap1 = [[], []]
    rectMap2 = [[], []]
    rectMap1[0], rectMap1[1] = cv2.initUndistortRectifyMap(K1, D1, Rrect1, P1, newsize, cv2.CV_16SC2)
    rectMap2[0], rectMap2[1] = cv2.initUndistortRectifyMap(K2, D2, Rrect2, P2, newsize, cv2.CV_16SC2)

    # Apply rectification
    img1, _ = dataio.imread(imgpath1)
    img2, _ = dataio.imread(imgpath2)
    # img1 = cv2.resize(img1, (img1.shape[1] / 2, img1.shape[0] / 2), interpolation=cv2.INTER_LANCZOS4)
    # img2 = cv2.resize(img2, (img2.shape[1] / 2, img2.shape[0] / 2), interpolation=cv2.INTER_LANCZOS4)
    imgRect1 = cv2.remap(img1, rectMap1[0], rectMap1[1], cv2.INTER_CUBIC)
    imgRect2 = cv2.remap(img2, rectMap2[0], rectMap2[1], cv2.INTER_CUBIC)

    # Save images
    filename1, file_extension1 = os.path.splitext(imgpath1)
    dataio.imwrite(filename1 + '_rect' + file_extension1, imgRect1)
    filename2, file_extension2 = os.path.splitext(imgpath2)
    dataio.imwrite(filename2 + '_rect' + file_extension2, imgRect2)

    # img_l, gray_l = getimage(imgpath1)
    # img_r, gray_r = getimage(imgpath2)
    #
    # imgorig_l = utils.resizeimgh(img_l, H_IMGS)
    # imgorig_r = utils.resizeimgh(img_r, H_IMGS)
    # imgorig = np.hstack((imgorig_l, imgorig_r))
    #
    # imgRect_l = cv2.remap(img_l, rectMap1[0], rectMap1[1], cv2.INTER_CUBIC)
    # imgRect_r = cv2.remap(img_r, rectMap2[0], rectMap2[1], cv2.INTER_CUBIC)
    #
    # imgtoshow_l = utils.resizeimgh(imgRect_l, H_IMGS)
    # imgtoshow_r = utils.resizeimgh(imgRect_r, H_IMGS)
    # imgtoshow = np.hstack((imgtoshow_l, imgtoshow_r))
    #
    # lines = [((0, int(r)), (imgtoshow.shape[1], int(r)), (uniform(0, 255), uniform(0, 255), uniform(0, 255))) for r in np.linspace(0, imgtoshow.shape[0], 20)]
    # for pt in lines:
    #     cv2.line(imgtoshow, pt[0], pt[1], pt[2], 1)
    #
    # imgtoshow = np.vstack((utils.resizeimgw(imgorig, W_IMGS), utils.resizeimgw(imgtoshow, W_IMGS)))
    #
    # filename1, file_extension1 = os.path.splitext(imgpath1)
    # filename2, file_extension2 = os.path.splitext(imgpath2)
    #
    # # imgpathout = '/Users/giulio/Desktop/stereo/%s.png'
    # # dataio.imwrite(filename1 + '_rect' + file_extension1, imgRect_l)
    # # dataio.imwrite(filename2 + '_rect' + file_extension2, imgRect_r)
    # figure_key_press()
    # plt.imshow(imgtoshow)
    # plt.show()