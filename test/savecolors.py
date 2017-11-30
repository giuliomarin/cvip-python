from cvip import *
from matplotlib.pylab import cm
import numpy as np

def savescale(img, img_pathout, minmax = (0, 1), mask = None, colmap = None):
    imgCrop = img
    if len(imgCrop.shape) < 3:
        imgCrop = (imgCrop - minmax[0]) / float(minmax[1] - minmax[0]) * 255
        imgCrop[imgCrop < 0] = 0
        imgCrop[imgCrop > 255] = 255
    if not mask is None:
        imgCrop[~mask] = 0
    dataio.imwrite(img_pathout, imgCrop, colmap)

f = '/Users/giulio/Desktop/GT/%s%d.png'
for e in range(2, 13):
    p = f % ('', e)
    img = dataio.opencv2matplotlib(dataio.imread(p)[0])
    vv = []
    for v in img.flatten():
        if v > 0:
            vv.append(v)
    minv = np.percentile(np.asarray(vv), 1) - 2
    maxv = np.percentile(np.asarray(vv), 99) + 2
    savescale(img, f % ('disp_', e), minmax = (minv, maxv), colmap = cm.jet_r)