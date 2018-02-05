from cvip import ymlparser, xmlparser, utils, transformations
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

calibyml = 0

calibPath = '/Data/1_seat/calibration/2018_01_19_15_41_31/front/ProcessedCalib/extrinsics2.xml'
planePath = "/Data/1_seat/calibration/2018_01_19_15_41_31/front/ProcessedCalib/groundPlane2.xml"

if calibyml:
    calib = ymlparser.parse(calibPath)
    ncam = calib['numCameras']
else:
    calib = xmlparser.parse(calibPath)
    ncam = int(xmlparser.get(calib, ['numCameras']))

if len(planePath) > 0:
    plane = xmlparser.parse(planePath)
    Rp = xmlparser.get(plane, ['R'])
    Tp = xmlparser.get(plane, ['T'])
else:
    Rp = np.eye(3)
    Tp = np.zeros((3, 1))

fig = plt.figure('camera')
ax = Axes3D(fig)

# List of colors (1=red, 2=green, 4=blue)
# colorSequence = range(ncam)
# shuffle(colorSequence)
colorSequence = [1, 2, 4, 3, 0]
for c, color in enumerate(colorSequence):
    camera = 'camera_%d' % c
    if calibyml:
        cam = calib['camera_calibrations'][camera]
        K = cam['K']
        R = cam['R']
        T = cam['T']
        width = cam['resolution'][0]
        height = cam['resolution'][1]
    else:
        K = xmlparser.get(calib, ['camera_calibrations', camera, 'K'])
        R = xmlparser.get(calib, ['camera_calibrations', camera, 'R'])
        T = xmlparser.get(calib, ['camera_calibrations', camera, 'T'])
        res = xmlparser.get(calib, ['camera_calibrations', camera, 'resolution']).split()
        width = int(res[0])
        height = int(res[1])

    # Refer to plane
    Rpinv = Rp.transpose()
    Tpinv = -Rpinv.dot(Tp)
    Rc = R.dot(Rpinv)
    Tc = R.dot(Tpinv) + T

    RR = np.eye(4)
    RR[:3, :3] = Rc
    # print transformations.rotation_from_matrix(RR)[0] / np.pi * 180
    focal = K[0, 0]
    Rinv = Rc.transpose()
    Tinv = -Rinv.dot(Tc)
    utils.plotcam(ax, Rinv, Tinv.transpose(),
                  col=[(color & 1) > 0, (color & 2) > 0, (color & 4) > 0],
                  scale=2e-1, h=height, w=width, f=focal)
    # ax.scatter(0, 0, 500, c='r', linewidth=2.0)

    if len(planePath) > 0:
        Rpinv = np.eye(3)
        Tpinv = np.zeros((3, 1))
        utils.plotplane(ax, Rpinv, Tpinv.transpose(), w=210.0, h=297.0)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
s = 700
ax.set_xlim((-s, s))
ax.set_ylim((-s, s))
ax.set_zlim((-s/2, s*3/2))
plt.show()
