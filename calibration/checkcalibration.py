import os
from cvip import ymlparser, dataio
import numpy as np
import matplotlib.pyplot as plt
import cv2


def inv(M):
    R = M[:3, :3]
    T = M[:3, 3]
    Minv = np.eye(4)
    Minv[:3, :3] = R.transpose()
    Minv[:3, 3] = -R.transpose().dot(T)
    return Minv


def drawCheckerboard(img, K, R, T, nx=10, ny=8, sx=20, sy=20):
    for xx in range(nx):
        for yy in range(ny):
            p3d = np.asarray([xx * sx, yy * sy, 0]).reshape(3, -1)
            p3dcam = R.dot(p3d) + T
            p2dh = K.dot(p3dcam) / p3dcam[2]
            p2d = np.asarray(p2dh[:2], dtype=int)
            size = 8 if img.shape[0] > 500 else 3
            cv2.circle(img, tuple(p2d), size, (255, 0, 0), -1)
    return img


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


if __name__ == '__main__':

    sensor = 'kinect_r200_zed'
    imgsDir = '/Data/0_Dataset/multicam/calib/6'

    if sensor == 'kinect':
        img_names = ['img_r1_s1_1.png', 'img_r1_s1_2.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_kinect.yml'
    elif sensor == 'zed':
        img_names = ['img_r1_s4_1.png', 'img_r1_s4_2.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_zed.yml'
    elif sensor == 'kinect2zed':
        img_names = ['img_r1_s1_1.png', 'img_r1_s4_1.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_kinect2zed.yml'
    elif sensor == 'kinect_zed':
        img_names = ['img_r1_s1_1.png', 'img_r1_s1_2.png', 'img_r1_s4_1.png', 'img_r1_s4_2.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_kinect_zed.yml'
    elif sensor == 'r200':
        img_names = ['img_r1_s2_1.png', 'img_r1_s2_2.png', 'img_r1_s2_3.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_r200.yml'
    elif sensor == 'kinect_r200_zed':
        img_names = ['img_r1_s1_c1.png', 'img_r1_s1_c2.png', 'img_r1_s2_c1.png', 'img_r1_s2_c2.png', 'img_r1_s2_c3.png', 'img_r1_s4_c1.png', 'img_r1_s4_c2.png']
        calibPath = '/Data/0_Dataset/multicam_out/calib_s1_s2_s3.yml'

    calib = ymlparser.parse(calibPath)

    for c in range(calib['numCameras']):

        # Load calib
        camera = 'camera_%d' % c
        cam = calib['camera_calibrations'][camera]
        K = cam['K']
        D = cam['D']
        R = cam['R']
        T = cam['T']
        width = cam['resolution'][0]
        height = cam['resolution'][1]

        # Load image
        img_path = os.path.join(imgsDir, img_names[c])
        # img_path = os.path.join(imgsDir, 'img_r1_s1_%d.png' % (c + 1))
        img, _ = dataio.imread(img_path)
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            img = img.astype(np.float32) - np.min(img)
            img = img / np.max(img) * 255.0
            img = img.astype(np.uint8)
            gray = img
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Undistortion
        Knew, roi = cv2.getOptimalNewCameraMatrix(K, D, (width, height), 1, (width, height))
        mapx, mapy = cv2.initUndistortRectifyMap(K, D, None, K, (width, height), 5)
        imgund = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        if c == 0:

            # Find the chess board corners
            N_CHECKERS = (10, 8)  # (points_per_row,points_per_colum)
            ret, corners = cv2.findChessboardCorners(gray, N_CHECKERS, None, flags=cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

            # If not found skip impage
            if ret is not True:
                print ' [not found]'
            else:
                print ' [found]'

                # refinine image points using subpixel accuracy
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.01))

                # Find the rotation and translation vectors.
                objp = np.zeros((np.prod(N_CHECKERS), 3), np.float32)
                objp[:, :2] = np.mgrid[0:N_CHECKERS[0], 0:N_CHECKERS[1]].T.reshape(-1, 2)
                objp *= 20.0

                axis = np.float32([[20*(N_CHECKERS[0]-1), 0, 0], [0, 20*(N_CHECKERS[1]-1), 0], [0, 0, -20*(N_CHECKERS[0]-1)]]).reshape(-1, 3)
                _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, K, D)
                rmat, _ = cv2.Rodrigues(rvecs)

                RTcheck = np.eye(4)
                RTcheck[:3, :3] = rmat
                RTcheck[:3, 3] = tvecs.transpose()

                imgund = drawCheckerboard(imgund, K, rmat, tvecs, sx=20, sy=20)
        else:
            RT = np.eye(4)
            RT[:3, :3] = R
            RT[:3, 3] = T.transpose()

            RTtot = RT.dot(RTcheck)
            Rtot = RTtot[:3, :3]
            Ttot = RTtot[:3, 3].reshape(3, 1)

            imgund = drawCheckerboard(imgund, K, Rtot, Ttot, sx=20, sy=20)

        # plt.figure(camera)
        # plt.imshow(imgund)
        # plt.savefig('/Data/0_Dataset/multicam/calib_characterization/%s.png' % camera)
        plt.imsave('/Data/0_Dataset/multicam/calib_characterization/%s.png' % camera, imgund)
    # plt.show()

