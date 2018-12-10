import numpy as np
from cvip import dataio
import matplotlib.pyplot as plt

imgpath = '/Data/13_calibration/Wall/%d/sir/Depth/depth_%d.png'

imgs = []
for f in range(1, 7):

    def prepareimg(imgpath):
        img = dataio.imread(imgpath)[0]
        img[img <= 0] = np.nan
        return img[140:365, 215:490]

    imgAvg = img = prepareimg(imgpath % (f, 1))

    num = 1
    for i in range(2, 25):
        num += 1
        img = prepareimg(imgpath % (f, i))
        imgAvg += img
        imgs = np.append(imgs, np.squeeze(img))

    imgAvg /= num
    avgD = np.nanmean(imgAvg)
    minD = np.nanmin(imgAvg)
    maxD = np.nanmax(imgAvg)
    stdD = np.nanstd(imgAvg)
    print avgD, stdD, minD, maxD
    imgAvg -= avgD

    plt.figure('bias %d ' % f)
    plt.imshow(imgAvg)
    plt.title('avg: %.2f std: %.2f min: %.2f max: %.2f\n' % (avgD, stdD, minD, maxD))
    plt.colorbar()
    plt.set_cmap('Reds')
    distRange = 0.03 * avgD
    plt.clim(-distRange, distRange)
    plt.savefig("/Users/giulio/Desktop/box/depth_%d.png" % f, bbox_inches='tight')


plt.figure()
imgs = imgs[~np.isnan(imgs)]
plt.hist(imgs, bins=300, normed=True)
plt.title('histogram')
plt.xlabel('Distance')
plt.ylabel('Distribution')
plt.xlim((0, 3200))
plt.savefig("/Users/giulio/Desktop/box/histogram.png", bbox_inches='tight')