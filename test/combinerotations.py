from cvip import transformations as tf
from cvip import ymlparser as yml
from cvip import xmlparser as xml
from calibration import utils as calib_utils
import numpy as np
import xmltodict

if 0:
    calib_kinect = yml.parse('/Data/0_Dataset/multicam_out/calib_kinect.yml')
    calib_zed = yml.parse('/Data/0_Dataset/multicam_out/calib_zed.yml')
    calib_r200 = yml.parse('/Data/0_Dataset/multicam_out/calib_r200.yml')
    calib_kinect_zed = yml.parse('/Data/0_Dataset/multicam_out/calib_kinect2zed.yml')
    calib_kinect_r200 = yml.parse('/Data/0_Dataset/multicam_out/calib_kinect2r200.yml')

    print 'zed'
    cam = calib_kinect_zed['camera_calibrations']['camera_1']
    R_kinect_zed = cam['R']
    T_kinect_zed = cam['T']
    RT_kinect_zed = np.eye(4)
    RT_kinect_zed[:3, :3] = R_kinect_zed
    RT_kinect_zed[:3, 3] = T_kinect_zed.transpose()

    print 'camera_0'
    cam = calib_zed['camera_calibrations']['camera_0']
    R_zed0 = cam['R']
    T_zed0 = cam['T']
    RT_zed0= np.eye(4)
    RT_zed0[:3, :3] = R_zed0
    RT_zed0[:3, 3] = T_zed0.transpose()

    RT_zed0_new = RT_kinect_zed.dot(RT_zed0)
    print RT_zed0_new[:3, :3]
    print RT_zed0_new[:3, 3]

    print 'camera_1'
    cam = calib_zed['camera_calibrations']['camera_1']
    R_zed1 = cam['R']
    T_zed1 = cam['T']
    RT_zed1 = np.eye(4)
    RT_zed1[:3, :3] = R_zed1
    RT_zed1[:3, 3] = T_zed1.transpose()

    RT_zed1_new = RT_zed0_new.dot(RT_zed1)
    print RT_zed1_new[:3, :3]
    print RT_zed1_new[:3, 3]

    print 'r200'
    cam = calib_kinect_r200['camera_calibrations']['camera_1']
    R_kinect_r200 = cam['R']
    T_kinect_r200 = cam['T']
    RT_kinect_r200 = np.eye(4)
    RT_kinect_r200[:3, :3] = R_kinect_r200
    RT_kinect_r200[:3, 3] = T_kinect_r200.transpose()

    print 'camera_0'
    cam = calib_r200['camera_calibrations']['camera_0']
    R_r2000 = cam['R']
    T_r2000 = cam['T']
    RT_r2000 = np.eye(4)
    RT_r2000[:3, :3] = R_r2000
    RT_r2000[:3, 3] = T_r2000.transpose()

    RT_r2000_new = RT_kinect_r200.dot(RT_r2000)
    print RT_r2000_new[:3, :3]
    print RT_r2000_new[:3, 3]

    print 'camera_1'
    cam = calib_r200['camera_calibrations']['camera_1']
    R_r2001 = cam['R']
    T_r2001 = cam['T']
    RT_r2001 = np.eye(4)
    RT_r2001[:3, :3] = R_r2001
    RT_r2001[:3, 3] = T_r2001.transpose()

    RT_r2001_new = RT_r2000_new.dot(RT_r2001)
    print RT_r2001_new[:3, :3]
    print RT_r2001_new[:3, 3]

    print 'camera_2'
    cam = calib_r200['camera_calibrations']['camera_2']
    R_r2002 = cam['R']
    T_r2002 = cam['T']
    RT_r2002 = np.eye(4)
    RT_r2002[:3, :3] = R_r2002
    RT_r2002[:3, 3] = T_r2002.transpose()

    RT_r2002_new = RT_r2000_new.dot(RT_r2002)
    print RT_r2002_new[:3, :3]
    print RT_r2002_new[:3, 3]
if 0:
    for v in [[0, 1, 0, 0.01], [0, 1, 0, 90], [0, 1, 0, 180], [0, 1, 0, 270], [1, 0, 0, 90], [1, 0, 0, -90]]:
        m1 = tf.rotation_matrix(np.deg2rad(180), [0, 0, 1])
        m2 = tf.rotation_matrix(np.deg2rad(v[3]), [v[0], v[1], v[2]])
        m = np.dot(m1, m2)
        angle, direction, point = tf.rotation_from_matrix(m)
        print "[%.3f, %.3f, %.3f, %d]" % (direction[0], direction[1], direction[2], np.rad2deg(angle))

if 0:
    calibPath = '/Users/giulio/Desktop/collection_20161002/out/calib_all.yml'
    R1 = yml.getInfoFromNodePath(calibPath, ['camera_calibrations', 'camera_2', 'R'])
    T1 = yml.getInfoFromNodePath(calibPath, ['camera_calibrations', 'camera_2', 'T'])
    R2 = yml.getInfoFromNodePath(calibPath, ['camera_calibrations', 'camera_3', 'R'])
    T2 = yml.getInfoFromNodePath(calibPath, ['camera_calibrations', 'camera_3', 'T'])

    R = R2.dot(np.linalg.inv(R1))
    T = T2 - R2.dot(np.linalg.inv(R1)).dot(T1)

    print R
    print
    print T

if 0:
    calib = '/Data/9_pg/c4_3cam_20170824/ProcessedCalib/groundPlane00.xml'
    R = xml.get(xml.parse(calib), ['R'])
    T = xml.get(xml.parse(calib), ['T'])
    Rrot = tf.rotation_matrix(-np.pi / 2., R[2,:], [T[0][0], T[1][0], T[2][0]])[0:3, 0:3]
    print R
    print Rrot
    Rnew = R.dot(Rrot)
    print Rnew
    print
    Trot = np.asarray([-420., -490., 0]).reshape(3, 1)
    Trot = np.asarray([0., 1200., 0]).reshape(3, 1)
    # Trot = R.transpose().dot(Trot)
    Tnew = T + Trot
    print T.transpose()
    print Trot.transpose()
    print Tnew.transpose()

if 1:
    # Parameters
    offset = [0, 100, 0]
    planeCalibPath = "/Data/1_seat/magna1/2018_06_04_06_54_15/front/ProcessedCalib/groundPlane2.xml"

    # Get current RT
    calib = xml.parse(planeCalibPath)
    R = xml.get(calib, ['R'])
    T = xml.get(calib, ['T'])
    RT = np.eye(4)
    RT[:3, :3] = R
    RT[:3, 3] = T.reshape(3)

    # Apply offset
    offsetRT = np.eye(4)
    offsetRT[:3, 3] = np.array(offset)
    RT = RT.dot(offsetRT)

    # Save data
    xml.set(calib, ['R'], RT[:3, :3])
    xml.set(calib, ['T'], RT[:3, 3])
    xml.write(calib, planeCalibPath.replace(".xml", "_new.xml"))
