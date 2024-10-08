from cvip import dataio
from matplotlib.pylab import cm
import numpy as np
import sys


def cropandsave(img, img_pathout, roi=None, minmax=(0., 1.), mask=None, colmap=None):
    """
    Crop and save the image after the processing specified by the parameters.

    :param img: input image.
    :param img_pathout: output image path.
    :param roi: output roi.
    :param minmax: min and max color value.
    :param mask: optional output mask.
    :param colmap: optional color map.
    """
    imgCrop = img
    if len(imgCrop.shape) < 3:
        imgCrop = (imgCrop - minmax[0]) / float(minmax[1] - minmax[0]) * 255
        imgCrop[imgCrop < 0] = 0
        imgCrop[imgCrop > 255] = 255
    if mask is not None:
        imgCrop[~mask] = 0
    if roi is not None:
        imgCrop = imgCrop[roi[0][0]:roi[0][1], roi[1][0]:roi[1][1]]
    # imgCrop[imgCrop <= 0] = 255
    dataio.imwrite(img_pathout, imgCrop.astype(np.uint8), colmap)

if __name__ == '__main__':
    n = 4
    if n == 5:
        print("Reading: %s" % sys.argv[1])
        img = dataio.imread(sys.argv[1])[0]
        imgVals = img.copy()
        imgVals[img <= 0] = np.nan
        minv = np.nanpercentile(imgVals, 1)
        maxv = np.nanpercentile(imgVals, 99)
        print("Min: %f Max: %f" % (minv, maxv))
        if len(sys.argv) == 3:
            outfile = sys.argv[2]
        else:
            outfile = sys.argv[1].replace('.png', '_viz.png')
        cropandsave(img, outfile,
                    None,
                    (minv, maxv),
                    None,
                    cm.jet)
    if n == 4:
        print("Reading: %s" % sys.argv[1])
        img = dataio.imread(sys.argv[1])[0]
        imgVals = img.copy()
        imgVals[img <= 0] = np.nan
        minv = np.nanpercentile(imgVals, 1)
        maxv = np.nanpercentile(imgVals, 99)
        print("Min: %f Max: %f" % (minv, maxv))
        if len(sys.argv) >= 4:
            minv = float(sys.argv[2])
            maxv = float(sys.argv[3])
            print("Min: %f Max: %f" % (minv, maxv))
        if len(sys.argv) == 5:
            outfile = sys.argv[4]
        else:
            outfile = sys.argv[1].replace('.tiff', '_viz.png')
        cropandsave(img, outfile,
                    None,
                    (minv, maxv),
                    None,
                    cm.jet)
    if n == 3:
        img = dataio.imread(sys.argv[1])[0]
        imgVals = img.copy()
        imgVals[img <= 0] = np.nan
        minv = np.nanpercentile(imgVals, 1)
        maxv = np.nanpercentile(imgVals, 99)
        print("Min: %f Max: %f" % (minv, maxv))
        # minv = 0
        # maxv = 100
        cropandsave(img, sys.argv[1].replace('.png', '_viz.png'),
                            None,
                            (minv, maxv),
                            None,
                            cm.jet)
    elif n == 2:
        for i in range(1, 11):
            p = '/Users/giulio/Dropbox (Personal)/Temporary/multicam/%d/img_r10_s2_c3.png' % i
            img = dataio.imread(p)[0] / 1000.
            dataio.imwrite(p, img)
    elif n == 1:
        for i in range(11):
            p = '/Data/0_Dataset/multicam_out/%d/img_r10_s2_c1.png' % i
            img = dataio.imread(p)[0]
            cropandsave(img,
                        p.replace('.png', '_viz.png'),
                        None,
                        (0, 65000),
                        None)
    elif n == 0:
        for c in range(1, 3):
            for i in range(1, 11):
                p = '/Data/0_Dataset/multicam_out/%d/gt_s1_c%d_small.png' % (i, c)
                img = dataio.imread(p)[0]
                valid_img = np.ma.masked_where(img <= 0, img).compressed()
                minv = np.percentile(valid_img, 1) - 2
                maxv = np.percentile(valid_img, 99) + 2
                cropandsave(img,
                            p.replace('.png', '_viz.png'),
                            None,
                            (minv, maxv),
                            None,
                            cm.jet_r)
