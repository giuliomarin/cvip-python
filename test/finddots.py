import cv2
from cvip import dataio
from matplotlib import pyplot as plt
import numpy as np

def process(camid):
    if camid == 0:
        img = dataio.imread("/Users/giulio/Desktop/aptina_vs_21/2/21.png")[0]
        minDot = 70
        cam = "2.1"
        radmask = 4
    elif camid == 1:
        img = dataio.imread("/Users/giulio/Desktop/aptina_vs_21/2/31_1.png")[0]
        minDot = 120
        cam = "3.1 scale 1"
        radmask = 4
    elif camid == 2:
        img = dataio.imread("/Users/giulio/Desktop/aptina_vs_21/2/31_1_5.png")[0]
        minDot = 120
        cam = "3.1 scale 1.5"
        radmask = 3
    elif camid == 3:
        img = dataio.imread("/Users/giulio/Desktop/aptina_vs_21/2/31_1_7.png")[0]
        minDot = 120
        cam = "3.1 scale 1.7"
        radmask = 3.5
    elif camid == 4:
        img = dataio.imread("/Users/giulio/Desktop/aptina_vs_21/Snapshot1/sir/Rectified/masterRect_1.png")[0]
        minDot = 120
        cam = "3.1 scale 1"
        radmask = 3.5

    viz = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    dots = np.zeros(img.shape, np.uint8)

    numDots = 0
    while True:
        imgmin, imgmax, _, maxLoc = cv2.minMaxLoc(img)
        # print 'MaxLoc: (%d, %d) - Min [%f] - Max [%f]' % (maxLoc[0], maxLoc[1], imgmin, imgmax)

        if imgmax < minDot:
            break

        img[int(round(max(0, maxLoc[1]-radmask))):int(round(min(maxLoc[1]+radmask, img.shape[0]))), int(round(max(0, maxLoc[0]-radmask))):int(round(min(maxLoc[0]+radmask, img.shape[1])))] = 0
        dots[int(round(max(0, min(maxLoc[1], img.shape[0])))), int(round(max(0, min(maxLoc[0], img.shape[1]))))] = 255
        rad = 0.5
        viz[max(0, int(round(maxLoc[1] - rad))):min(int(round(maxLoc[1] + rad)), img.shape[0]), max(0, int(round(maxLoc[0] - rad))):min(int(round(maxLoc[0] + rad)), img.shape[1]), 0] = 255
        viz[max(0, int(round(maxLoc[1] - rad))):min(int(round(maxLoc[1] + rad)), img.shape[0]), max(0, int(round(maxLoc[0] - rad))):min(int(round(maxLoc[0] + rad)), img.shape[1]), 1] = 0
        viz[max(0, int(round(maxLoc[1] - rad))):min(int(round(maxLoc[1] + rad)), img.shape[0]), max(0, int(round(maxLoc[0] - rad))):min(int(round(maxLoc[0] + rad)), img.shape[1]), 2] = 0
        numDots += 1
        # if numDots % 100 == 0:
        #     plt.imshow(img, cmap="gray")
        #     plt.draw()
        #     plt.waitforbuttonpress()

    print "Num dots: %d" % numDots

    dist = cv2.distanceTransform(1 - dots / 255, cv2.DIST_L2, 3)
    dist = dist / 8 * 255
    dist = dist.astype(np.uint8)

    plt.imsave("/Users/giulio/Desktop/aptina_vs_21/2/2_%d_1_%d.png" % (camid, numDots), dots, cmap="gray")
    plt.imsave("/Users/giulio/Desktop/aptina_vs_21/2/2_%d_2_%d.png" % (camid, numDots), dist, cmap="jet")
    plt.imsave("/Users/giulio/Desktop/aptina_vs_21/2/2_%d_0_%d.png" % (camid, numDots), viz)
    # plt.figure("[%s] distance" % cam); plt.imshow(dist, cmap="gray")
    # plt.figure("[%s] mask" % cam); plt.imshow(viz)
    # plt.figure("[%s] %d dots" % (cam, numDots)); plt.imshow(dots, cmap="gray")
    # plt.show()

process(4)
# for camid in range(4):
#     process(camid)