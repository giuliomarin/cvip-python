from cvip import ymlparser, utils, transformations
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

calibPath = r'/Users/giulio/Desktop/collection_20161002/out/calib_all.yml'
calib = ymlparser.parse(calibPath)

fig = plt.figure('camera')
ax = Axes3D(fig)

# List of colors (1=red, 2=green, 4=blue)
colorSequence = [1, 1, 2, 2, 2, 4, 4]
for c, color in enumerate(colorSequence):
    cam = calib['camera_calibrations']['camera_%d' % c]
    K = cam['K']
    R = cam['R']
    T = cam['T']
    # RR = np.eye(4)
    # RR[:3, :3] = R
    # print transformations.rotation_from_matrix(RR)[0] / np.pi * 180
    width = cam['resolution'][0]
    height = cam['resolution'][1]
    focal = K[0, 0]
    print K[1, 2]
    utils.plotcam(ax, R, T.transpose(),
                  col = [(color & 1) > 0, (color & 2) > 0, (color & 4) > 0],
                  scale = 3e-2, h = height, w = width, f = focal)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim((-100, 100))
ax.set_ylim((-100, 100))
ax.set_zlim((-100, 100))
ax.autoscale_view()
plt.show()
