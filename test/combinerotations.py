from cvip import transformations as tf
import numpy as np

for v in [[0, 1, 0, 0.01], [0, 1, 0, 90], [0, 1, 0, 180], [0, 1, 0, 270], [1, 0, 0, 90], [1, 0, 0, -90]]:
    m1 = tf.rotation_matrix(np.deg2rad(180), [0, 0, 1])
    m2 = tf.rotation_matrix(np.deg2rad(v[3]), [v[0], v[1], v[2]])
    m = np.dot(m1, m2)
    angle, direction, point = tf.rotation_from_matrix(m)
    print "[%.3f, %.3f, %.3f, %d]" % (direction[0], direction[1], direction[2], np.rad2deg(angle))