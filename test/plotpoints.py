import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure('points')
ax = Axes3D(fig)


#
# # plot vector
# pp = np.asarray(np.loadtxt('/GitHub/Nitrogen_Build/bin/RelWithDebInfo/points.txt'))
# ax.scatter(pp[:, 0], pp[:, 1], pp[:, 2], s = 1, edgecolors = 'face', alpha = 0.3)
# data = pp[:, 2]
# minz = min(data)
# maxz = max(data)
# slots = np.arange(minz, maxz, 0.1)
# bin = [0] * len(slots)
# for e in data:
#     minDist = float('inf')
#     idx = -1
#     for i, s in enumerate(slots):
#         if abs(e - s) < minDist:
#             minDist = abs(e - s)
#             idx = i
#     bin[idx] += 1
# print bin
# # plt.plot(range(len(bin)), bin)
# plt.show()
# quit()

pp = np.asarray(np.loadtxt('/GitHub/Nitrogen_Build/bin/RelWithDebInfo/axis1.txt'))
ax.scatter(pp[:, 0], pp[:, 1], pp[:, 2], s = 1, c = 'b', edgecolors = 'face', alpha = 0.3)

pp = np.asarray(np.loadtxt('/GitHub/Nitrogen_Build/bin/RelWithDebInfo/axis2.txt'))
ax.scatter(pp[:, 0], pp[:, 1], pp[:, 2], s = 1, c = 'k', edgecolors = 'face', alpha = 0.3)

# plot axes
aa = np.asarray(np.loadtxt('/GitHub/Nitrogen_Build/bin/RelWithDebInfo/axes.txt'))
ax.plot([-aa[0, 0],aa[0, 0]], [-aa[0, 1],aa[0, 1]], [-aa[0, 2],aa[0, 2]], linewidth = 2.0)
ax.plot([-aa[1, 0],aa[1, 0]], [-aa[1, 1],aa[1, 1]], [-aa[1, 2],aa[1, 2]], linewidth = 2.0)
ax.plot([-aa[2, 0],aa[2, 0]], [-aa[2, 1],aa[2, 1]], [-aa[2, 2],aa[2, 2]], linewidth = 2.0)

# plot directions
dd = np.asarray(np.loadtxt('/GitHub/Nitrogen_Build/bin/RelWithDebInfo/dir.txt'))
dd[:, 3] = dd[:, 3] / max(dd[:, 3]) * 100
ax.scatter(dd[:, 0], dd[:, 1], dd[:, 2], s = dd[:, 3], c = 'r', edgecolors = 'face')

# # plot sphere
# u = np.linspace(0, 2 * np.pi, 100)
# v = np.linspace(0, np.pi, 100)
# s = 0.95
# x = s * np.outer(np.cos(u), np.sin(v))
# y = s * np.outer(np.sin(u), np.sin(v))
# z = s * np.outer(np.ones(np.size(u)), np.cos(v))
# ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim((-2, 2))
ax.set_ylim((-2, 2))
ax.set_zlim((-2, 2))
ax.set_aspect('equal')

plt.show()