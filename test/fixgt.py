from cvip import dataio
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np


def figure_key_press(*args, **kwargs):
    def on_key_press(event):
        if event.key == 'escape':
            exit(0)
    fig = plt.figure(*args, **kwargs)
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    return fig

for s in range(1, 11):
    p = '/Data/0_Dataset/multicam_out/%s/gt_s1_c2_small.png' % s
    img = dataio.imread(p)[0]

    vmin = 60
    vmax = 140

    # figure_key_press('orig')
    # plt.imshow(img, vmin=vmin, vmax=vmax)
    # plt.colorbar()

    img = ndimage.filters.median_filter(img, 3)
    # img_filt = ndimage.gaussian_filter(img, 2)
    # mask = np.ma.masked_where(abs(img - img_filt) < 3, img)
    # img[mask.mask] = img_filt[mask.mask]

    # figure_key_press(s)
    # plt.imshow(img, vmin=vmin, vmax=vmax)
    # plt.colorbar()

    # mask = (img < vmin) & (img > vmax)
    # img[mask] = np.nan
    # grad = np.gradient(img)
    # plt.figure('gradient')
    # plt.imshow(np.sqrt(grad[0] * grad[0] + grad[1] * grad[1]))
    # plt.colorbar()
    dataio.imwrite(p.replace('.png', '_filt.png'), img)

# plt.show()