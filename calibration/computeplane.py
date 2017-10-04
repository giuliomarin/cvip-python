from cvip import xmlparser
import numpy as np

calibpath = '/Data/9_pg/c4_3cam_20170824/ProcessedCalib/groundPlane0_0_1_2.xml'
calib = xmlparser.parse(calibpath)
R = xmlparser.get(calib, ['R'])
T = xmlparser.get(calib, ['T'])
groundPlane = xmlparser.get(calib, ['groundPlane'])

print R
print T
print groundPlane

Rinv = R.transpose()
Tinv = - Rinv.dot(T)

print ''
print Rinv
print Tinv
print ''

# RT = [R T] : rototranslation from camera to plane
# Ac = [a, b, c, d] : plane equation in camera reference system
# Ap = [aa, bb, cc, dd] : plane euqation in plane reference system
# pc : point in camera reference system
# pp = RT*pc : point in plane reference system

print R.dot(np.asmatrix([0, 0, 10000]).transpose()) + T
print Rinv.dot(np.asmatrix([0, 0, 10000]).transpose()) + Tinv