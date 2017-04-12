from cvip import dataio, ymlparser
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

# s = sys.argv[1]
s = '8'
img1 = dataio.imread('/Users/giulio/Desktop/stereo/%s.png' % s)[0]
img2 = dataio.imread('/Users/giulio/Desktop/collection_20161002/out/scene3/exp2/img_r1_s2_4.png')[0]

calibPath = r'/Users/giulio/Desktop/collection_20161002/out/calib_all.yml'
calib = ymlparser.parse(calibPath)

def projdepth(depth1, img2, K1, K2, R2, T2, squareradius = 0):
    K1i = np.linalg.inv(K1)
    depth1to2 = np.empty(img2.shape[:2], dtype = np.float32)
    zbuffer = np.full(img2.shape[:2], float('inf'), dtype=np.float32)
    for v in range(depth1.shape[0]):
        for u in range(depth1.shape[1]):
            z = depth1[v, u]
            if z <= 0:
                continue
            uvz = np.transpose(np.asmatrix([u * z, v * z, z]))

            # back project
            xyz = K1i.dot(uvz)

            # apply roto translation
            xyzRT = R2.dot(K1i.dot(uvz)) + T2

            # project on 2
            uvz2 = K2.dot(xyzRT)
            z2 = uvz2[2]
            c = int(uvz2[0] / z2 + 0.5)
            r = int(uvz2[1] / z2 + 0.5)

            # check if it is inside
            if not (squareradius < r < img2.shape[0] - squareradius and squareradius < c < img2.shape[1] - squareradius):
                continue

            # check z buffer
            for rr in range(r - squareradius, r + squareradius + 1):
                for cc in range(c - squareradius, c + squareradius + 1):
                    if zbuffer[rr, cc] > z2:
                        zbuffer[rr, cc] = z2
                        depth1to2[rr, cc] = z2
    return depth1to2

cam1 = calib['camera_calibrations']['camera_5']
K1 = cam1['K']
D1 = cam1['D']
R1 = cam1['R']
T1 = cam1['T']
cam2 = calib['camera_calibrations']['camera_2']
K2 = cam2['K']
D2 = cam1['D']
R2 = cam2['R']
T2 = cam2['T']

h, w = img1.shape[:2]
K1new, roi = cv2.getOptimalNewCameraMatrix(K1, D1, (w, h), 1, (w, h))
bf = 1.74659325e+05
K1new = np.asarray([[1.45550688e+03,   0.00000000e+00,  1.02495398e+03],
 [  0.00000000e+00,   1.45550688e+03,   5.91645039e+02],
 [  0.00000000e+00 ,  0.00000000e+00  , 1.00000000e+00]])

h, w = img2.shape[:2]
K2new, roi = cv2.getOptimalNewCameraMatrix(K2, D2, (w, h), 1, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(K2, D2, None, K2new, (img2.shape[1], img2.shape[0]), 5)
img2und = cv2.remap(img2, mapx, mapy, cv2.INTER_LINEAR)

# Compute relative transformation
RR = np.asarray([[ 0.99987272, -0.00137486,  0.015895  ],
 [ 0.00139923,  0.99999786 ,-0.00152249],
 [-0.01589288 , 0.00154454,  0.99987251]])
R1 = RR.dot(R1)
T1 = RR.dot(T1)
R12 = R2.dot(np.transpose(R1))
T12 = -R2.dot(np.transpose(R1).dot(T1)) + T2

depth1to2 = projdepth(img1, img2, K1new, K2new, R12, T12, 1)
dataio.imwrite32f('/Users/giulio/Desktop/stereoonr200/%s_new.png' % s, depth1to2)

# plt.figure('img1')
# plt.imshow(img1)
# plt.colorbar()
# plt.figure('img2 und')
# plt.imshow(img2und)
# plt.colorbar()
# plt.figure('depth1to2')
# plt.imshow(depth1to2)
# plt.colorbar()
# plt.show()