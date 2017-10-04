from cvip import transformations as tf
from cvip import ymlparser as yml
from cvip import xmlparser as xml
import numpy as np

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