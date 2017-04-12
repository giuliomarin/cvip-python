from cvip import transformations as tf
from cvip import ymlparser as yml
import numpy as np

if 0:
    for v in [[0, 1, 0, 0.01], [0, 1, 0, 90], [0, 1, 0, 180], [0, 1, 0, 270], [1, 0, 0, 90], [1, 0, 0, -90]]:
        m1 = tf.rotation_matrix(np.deg2rad(180), [0, 0, 1])
        m2 = tf.rotation_matrix(np.deg2rad(v[3]), [v[0], v[1], v[2]])
        m = np.dot(m1, m2)
        angle, direction, point = tf.rotation_from_matrix(m)
        print "[%.3f, %.3f, %.3f, %d]" % (direction[0], direction[1], direction[2], np.rad2deg(angle))

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