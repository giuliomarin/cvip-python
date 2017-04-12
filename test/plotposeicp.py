from cvip import ymlparser, utils, transformations
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mainPath = '/Users/giulio/Desktop/seat/2017_02_11_06_26_27/front'
calibPath = '%s/aligned/scanlivesToAlign.yml' % mainPath

calib = ymlparser.parse(calibPath)

fig = plt.figure('pose')
ax = Axes3D(fig)
plt.title(mainPath)

for c in range(calib['numScanlives']):
    trajectoryPath = r'%s/scanlives/scanlive%d/trajectory.yml' % (mainPath, c)
    trajectory = ymlparser.parse(trajectoryPath)

    # RT camera
    RT = calib['scanlives_calibrations']['view_%d' % c]['RT']
    Rc = RT[0:3, 0:3]
    Tc = RT[0:3, 3].reshape([3, 1])

    # Trajectory
    pos = []
    color = 4 # 1, 2, 4
    for v in range(0, trajectory['numViews']):
        view = trajectory['view_calibrations']['view_%d' % v]
        R = view['rotMat']
        T = view['tvec']
        width = 640.
        height = 480.
        focal = 800.
        # utils.plotcam(ax, R, T.transpose(), col = [(color & 1) > 0, (color & 2) > 0, (color & 4) > 0], scale = 3e-2, h = height, w = width, f = focal)
        Trot = Rc.dot(np.asarray(T)) + Tc
        # pos.append(T)
        pos.append(Trot)

    posA = np.asarray(pos)
    ax.plot3D(np.ravel(posA[:, 0]), np.ravel(posA[:, 1]), np.ravel(posA[:, 2]))

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim((-100, 800))
ax.set_ylim((-50, 50))
ax.set_zlim((-50, 50))
# ax.autoscale_view()
# ax.set_aspect('equal')
plt.show()
