from cvip import xmlparser as xml, transformations as tf
import utils
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

#######################
# Parameters
#######################

if len(sys.argv) == 3:
    calibNode1 = xml.parse(sys.argv[1])
    calibNode2 = xml.parse(sys.argv[2])
else:
    # calibNode1 = xml.parse('/Volumes/SensorsData/calibration/21_P_50C_00081/2019_01_26_02_51_59/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/Volumes/SensorsData/calibration/21_P_50C_00081/2019_01_26_04_18_02/CalibrationFile/ctgm020.xml')
    # calibNode1 = xml.parse('/data/13_calibration/phaser_v7/21_P_50C_00081/2018_12_19_23_47_32/CalibrationFile/ctgm020.xml')

    # calibNode1 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/0_calib/2019_02_09_00_30_33/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/0_calib/2019_02_09_00_39_34/CalibrationFile/ctgm020.xml')


    # calibNode1 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/0_calib/2019_02_09_00_39_34/CalibrationFile/ctgm020.xml')
    calibNode1 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/5_calib/2019_02_27_17_33_05/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/6_calib/from5/2019_02_28_17_29_26/CalibrationFile/ctgm020.xml')
    calibNode2 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/6_calib/2019_02_28_17_29_26/CalibrationFile/ctgm020.xml')


    # calibNode1 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/0_calib/2019_02_09_00_39_34/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/sens_49/21_P_50C_00075/3_calib/2019_02_22_21_11_21/CalibrationFile/ctgm020.xml')


    # calibNode1 = xml.parse('/data/13_calibration/phaser_v7/21_P_50C_00083/2018_12_19_05_50_08/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/phaser_v7/21_P_50C_00083/2019_01_10_19_20_55/CalibrationFile/ctgm020.xml')
    # calibNode1 = xml.parse('/data/13_calibration/phaser_v7/21_P_50C_00090/2018_12_20_22_54_04/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/phaser_v7/21_P_50C_00090/2019_01_22_02_18_28/CalibrationFile/ctgm020.xml')
    # calibNode1 = xml.parse('/data/13_calibration/nemo_over_time/21_N_52_C_00231/2019_01_25_21_41_23/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/nemo_over_time/21_N_52_C_00231/2019_01_25_21_42_09/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/nemo_over_time/21_N_52_C_00231/2019_01_25_21_42_47/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/nemo_over_time/21_N_52_C_00231/2019_01_25_21_45_11/CalibrationFile/ctgm020.xml')
    # calibNode2 = xml.parse('/data/13_calibration/nemo_over_time/21_N_52_C_00231/2019_01_25_21_46_25/CalibrationFile/ctgm020.xml')

#######################
# Main
#######################

# Loop all the cameras
for cam in range(int(xml.get(calibNode1, ['numCameras']))):
    # cameraname = ['master', 'slave', 'color']
    # camera = cameraname[cam]
    camera = "C%d" % cam

    #######################
    # Intrinsics
    #######################

    K1 = xml.get(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'K'])
    K2 = xml.get(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'K'])

    # Focal length and principal point
    fx = K2[0, 0] - K1[0, 0]
    fy = K2[1, 1] - K1[1, 1]
    cx = K2[0, 2] - K1[0, 2]
    cy = K2[1, 2] - K1[1, 2]

    #######################
    # Extrinsics
    #######################

    R1 = xml.get(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'R'])
    R2 = xml.get(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'R'])
    T1 = xml.get(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'T'])
    T2 = xml.get(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'T'])
    print (T2-T1)[0]

    R = np.eye(4)
    R[:3, :3] = R1[:3, :3]
    angle, direction, point = tf.rotation_from_matrix(R)
    _, _, angle, _, _ = tf.decompose_matrix(R)
    angle1 = angle[0]

    R = np.eye(4)
    R[:3, :3] = R2[:3, :3]
    angle, direction, point = tf.rotation_from_matrix(R)
    _, _, angle, _, _ = tf.decompose_matrix(R)
    angle2 = angle[0]
    print angle2 - angle1

    # Relative transformation
    RT1 = utils.createRT(R1, T1)
    RT2 = utils.createRT(R2, T2)
    RT12 = RT2.dot(utils.invRT(RT1))
    R = np.eye(4)
    R[:3, :3] = RT12[:3, :3]
    T = RT12[:3, 3]
    angle, direction, point = tf.rotation_from_matrix(R)
    _, _, angle, _, _= tf.decompose_matrix(R)
    angle = angle[0]


    #######################
    # Distortion
    #######################

    D1 = xml.get(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'D'])
    D2 = xml.get(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'D'])
    res = xml.get(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'resolution']).split()
    w, h = [int(res[0]), int(res[1])]

    mapx1, mapy1 = cv2.initUndistortRectifyMap(K1, D1, None, K1, (w, h), cv2.CV_32FC1)
    mapx2, mapy2 = cv2.initUndistortRectifyMap(K2, D2, None, K2, (w, h), cv2.CV_32FC1)
    mapDiff = np.sqrt((mapx2 - mapx1)**2 + (mapy2 - mapy1)**2)

    #######################
    # Show results
    #######################

    res = 'Camera: %s\n' \
          'fx = %+.3f px (%+.3f %%)  --  fy = %+.3f px (%+.3f %%)\n' \
          'cx = %+.3f px (%+.3f %%)  --  cy = %+.3f px (%+.3f %%)\n' \
          'r  = %+.3f deg  --  t  = %+.3f mm\n' % (camera, fx, fx / K1[0, 0] * 100., fy, fy / K1[1, 1] * 100., cx, cx / K1[0, 2] * 100., cy, cy / K1[1, 2] * 100., np.rad2deg(angle), np.linalg.norm(T))
    print res
    print 'D'
    print D2 - D1

    if 0:
        plt.figure(camera)
        plt.imshow(mapDiff)
        plt.colorbar()
        plt.set_cmap('Reds')
        plt.clim([0, 2])
        plt.title(res + 'Rectification map (|map2 - map1|) [px]')
        # plt.savefig('results_%s.pdf' % camera, bbox_inches='tight')

if 0:
    plt.figure()
    img = cv2.imread('/Volumes/RegressionTesting/SIR/RailTests/genericTests/AQP_Scanner/Calibration/01_27_2017/ThermalTest/30_Q_50C_00067_CalibrationHot/color0_2.png')
    imgund = cv2.remap(img, mapx2, mapy2, cv2.INTER_LINEAR)
    plt.imshow('undist', imgund)
plt.show()
