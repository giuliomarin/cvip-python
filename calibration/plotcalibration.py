from cvip import ymlparser, xmlparser, utils, transformations
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

calibyml = 0

calibPath = '/Users/giulio/Desktop/calib.xml'

if calibyml:
    calib = ymlparser.parse(calibPath)
    ncam = calib['numCameras']
else:
    calib = xmlparser.parse(calibPath)
    ncam = int(xmlparser.get(calib, ['numCameras']))

fig = plt.figure('camera')
ax = Axes3D(fig)

# List of colors (1=red, 2=green, 4=blue)
# colorSequence = range(ncam)
# shuffle(colorSequence)
colorSequence = [1] * ncam
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
    RR = np.eye(4)
    RR[:3, :3] = R
    print transformations.rotation_from_matrix(RR)[0] / np.pi * 180
    focal = K[0, 0]
    if c > 2:
        color = 2
    utils.plotcam(ax, R, T.transpose(),
                  col=[(color & 1) > 0, (color & 2) > 0, (color & 4) > 0],
                  scale=4e-1, h=height, w=width, f=focal)
    # ax.scatter(0, 0, 500, c='r', linewidth=2.0)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
s = 700
ax.set_xlim((-s, s))
ax.set_ylim((-s, s))
ax.set_zlim((-s, s))
ax.autoscale_view()
plt.show()
