import numpy as np
from cvip import dataio
import matplotlib.pyplot as plt

imgpath = '/Volumes/RegressionTesting/SIR/RailTests/genericTests/AQP_Scanner/WallTests/01_27_2017/FlatWall_30_Q_50C_00075_20170204-015805/DataFlatWall/%s/Depth/depth_%d.png'
dist = 1000

imgAvg = img = dataio.imread(imgpath % (dist, 1))[0]

num = 1
for i in range(2, 50):
    num += 1
    img = dataio.imread(imgpath % (dist, i))[0]
    img[img <= 0] = np.nan
    imgAvg += img

imgAvg /= num
avgD = np.nanmean(imgAvg)
minD = np.nanmin(imgAvg)
maxD = np.nanmax(imgAvg)
print avgD, minD, maxD
imgAvg -= avgD

plt.figure('bias')
plt.imshow(imgAvg)
plt.title('%s mm' % dist)
plt.colorbar()
plt.set_cmap('Reds')
distRange = 0.01 * dist
plt.clim(-distRange, distRange)
# plt.imsave("disp.png", img, cmap='Greys')

# plt.figure('average')
# plt.plot(np.nanmean(img, axis=0))
# # plt.plot(np.nanmean(img, axis=1))
plt.show()