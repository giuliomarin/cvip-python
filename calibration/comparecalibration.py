from cvip import xmlparser as xml, transformations as tf
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

#######################
# Parameters
#######################

if len(sys.argv) == 3:
    calibNode1 = xml.parse(sys.argv[1])
    calibNode2 = xml.parse(sys.argv[2])
else:
    calibNode1 = xml.parse('calib1.xml')
    calibNode2 = xml.parse('calib2.xml')

#######################
# Main
#######################

# Loop all the cameras
for cam in range(int(xml.getmat(calibNode1, ['numCameras']))):
    cameraname = ['master', 'slave', 'color']
    camera = cameraname[cam]

    #######################
    # Intrinsics
    #######################

    K1 = xml.getmat(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'K'])
    K2 = xml.getmat(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'K'])

    # Focal length and principal point
    fx = K1[0, 0] - K2[0, 0]
    fy = K1[1, 1] - K2[1, 1]
    cx = K1[0, 2] - K2[0, 2]
    cy = K1[1, 2] - K2[1, 2]

    #######################
    # Extrinsics
    #######################

    R1 = xml.getmat(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'R'])
    R2 = xml.getmat(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'R'])
    T1 = xml.getmat(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'T'])
    T2 = xml.getmat(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'T'])

    # Relative transformation
    R33 = R2.dot(np.linalg.inv(R1))
    T = T2 - R2.dot(np.linalg.inv(R1)).dot(T1)
    R = np.eye(4)
    R[:3, :3] = R33
    angle, direction, point = tf.rotation_from_matrix(R)

    #######################
    # Distortion
    #######################

    D1 = xml.getmat(calibNode1, ['camera_calibrations', 'camera_%d' % cam, 'D'])
    D2 = xml.getmat(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'D'])
    res = xml.getmat(calibNode2, ['camera_calibrations', 'camera_%d' % cam, 'resolution']).split()
    w, h = [int(res[0]), int(res[1])]

    mapx1, mapy1 = cv2.initUndistortRectifyMap(K1, D1, None, K1, (w, h), cv2.CV_32FC1)
    mapx2, mapy2 = cv2.initUndistortRectifyMap(K2, D2, None, K2, (w, h), cv2.CV_32FC1)
    mapDiff = np.sqrt((mapx1 - mapx2)**2 + (mapy1 - mapy2)**2)

    #######################
    # Show results
    #######################

    res = 'Camera: %s\n\n' \
          'fx = %+.1f px (%+.1f %%)  --  fy = %+.1f px (%+.1f %%)\n' \
          'cx = %+.1f px (%+.1f %%)  --  cy = %+.1f px (%+.1f %%)\n' \
          'r  = %+.1f deg  --  t  = %+.1f mm\n\n' % (camera, fx, fx / K1[0, 0] * 100., fy, fy / K1[1, 1] * 100., cx, cx / K1[0, 2] * 100., cy, cy / K1[1, 2] * 100., np.rad2deg(angle), np.linalg.norm(T))
    print res

    plt.figure(camera)
    plt.imshow(mapDiff)
    plt.colorbar()
    plt.set_cmap('Reds')
    plt.clim([0, 2])
    plt.title(res + 'Rectification map (|map1 - map2|) [px]')
    plt.savefig('results_%s.pdf' % camera, bbox_inches='tight')

plt.show()