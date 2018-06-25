from cvip import ymlparser
from cvip import xmlparser
from collections import OrderedDict
import numpy as np
import cv2

class CameraCalib(object):
    """
    Camera calibration
    """

    def __init__(self, resolution=None, K=None, D=None, R=None, T=None, camera_id=0, Rrect=None, P=None):
        self.resolution = resolution
        self.K = K
        self.D = D
        self.R = R
        self.T = T
        self.camera_id = camera_id
        self.Rrect = Rrect
        self.P = P

    def scale(self, scale=1.0):
        self.resolution *= scale
        self.K[:2, :] *= scale
        if self.P is not None:
            self.P[:2, :] *= scale

    def dict(self):
        dict = OrderedDict()
        dict['camera_id'] = self.camera_id
        dict['resolution'] = self.resolution
        dict['K'] = self.K
        dict['D'] = self.D
        dict['R'] = self.R
        dict['T'] = self.T
        dict['P'] = self.P
        dict['Rrect'] = self.Rrect
        return dict

    def __str__(self):
        txt = ''
        txt += 'camera_id: %s\n' % self.camera_id
        txt += 'resolution: %s\n' % self.resolution
        txt += 'K: %s\n' % self.K
        txt += 'D: %s\n' % self.D
        txt += 'R: %s\n' % self.R
        txt += 'T: %s\n' % self.T
        txt += 'P: %s\n' % self.P
        txt += 'Rrect: %s\n' % self.Rrect
        return txt


class SensorCalib(object):

    def __init__(self, calib_path, version=0):
        self.sensor_name = 'unknown'
        self.calib_time = ''
        self.camera_calib = {}
        self.read(calib_path, version)

    def read(self, calib_path, version=0):
        if version == 0:
            if calib_path.endswith('yml'):
                calib = ymlparser.parse(calib_path)
                self.sensor_name = calib['id']
                self.calib_time = calib['calibrationTime']
                for c in range(calib['numCameras']):
                    calib_cam = calib['camera_calibrations']['camera_%d' % c]
                    camera_calib = CameraCalib()
                    camera_calib.camera_id = calib_cam['camera_id']
                    camera_calib.resolution = np.array(calib_cam['resolution'], dtype=np.int)
                    camera_calib.K = calib_cam['K']
                    camera_calib.D = calib_cam['D']
                    camera_calib.R = calib_cam['R']
                    camera_calib.T = calib_cam['T']
                    if ymlparser.checkNodeExists(calib_cam, ['rectified_P']):
                        camera_calib.P = calib_cam['rectified_P']
                    if ymlparser.checkNodeExists(calib_cam, ['rectifying_rotation']):
                        camera_calib.Rrect = calib_cam['rectifying_rotation']
                    self.camera_calib[c] = camera_calib

            else:
                raise Exception('Extension not supported: %s.' % calib_path)
        elif version == 1:
            if calib_path.endswith('yml'):
                calib = ymlparser.parse(calib_path)
                self.sensor_name = calib['sensor_name']
                self.calib_time = calib['calib_time']
                for c in range(len(calib['camera_calib'])):
                    calib_cam = calib['camera_calib'][c]
                    camera_calib = CameraCalib()
                    camera_calib.camera_id = calib_cam['camera_id']
                    camera_calib.resolution = calib_cam['resolution'][0].astype(np.int)
                    camera_calib.K = calib_cam['K']
                    camera_calib.D = calib_cam['D']
                    camera_calib.R = calib_cam['R']
                    camera_calib.T = calib_cam['T']
                    if ymlparser.checkNodeExists(calib_cam, ['P']):
                        camera_calib.P = calib_cam['P']
                    if ymlparser.checkNodeExists(calib_cam, ['Rrect']):
                        camera_calib.Rrect = calib_cam['Rrect']
                    self.camera_calib[c] = camera_calib
            else:
                raise Exception('Extension not supported: %s.' % calib_path)
        else:
            raise Exception('Version %s not supported: %d.' % version)

    def write(self, calib_path, version=0):
        if version == 0:
            if calib_path.endswith('yml'):
                calib = OrderedDict()
                calib['sensor_name'] = self.sensor_name
                calib['calib_time'] = self.calib_time
                calib['camera_calib'] = self.camera_calib
                for c in calib['camera_calib']:
                    calib['camera_calib'][c] = calib['camera_calib'][c].dict()
                ymlparser.write(calib_path, OrderedDict(calib))
                pass
            else:
                raise Exception('Extension not supported: %s.' % calib_path)
        else:
            raise Exception('Version %s not supported: %d.' % version)

    def __str__(self):
        txt = ''
        txt += 'sensor_name: %s\n' % self.sensor_name
        txt += 'calib_time: %s\n' % self.calib_time
        for calib_cam in self.camera_calib:
            txt += str(self.camera_calib[calib_cam])
        return txt

def createRT(R, T):
    R = np.asarray(R)
    if R.shape[0] != 3 or R.shape[1] != 3:
        raise ValueError('R has wrong shape: (%d, %d)' % (R.shape[0], R.shape[1]))
    T = np.asarray(T)
    if len(T.ravel()) != 3:
        raise ValueError('T has wrong size: %d' % len(T.ravel()))
    RT = np.eye(4)
    RT[:3, :3] = R
    RT[:3, 3] = T.reshape(3)
    return RT

def invRT(M):
    if 3 > M.shape[0] > 4 or M.shape[1] != 4:
        raise ValueError('M has wrong shape: (%d, %d)' % (M.shape[0], M.shape[1]))
    R = M[:3, :3]
    T = M[:3, 3]
    Minv = np.eye(M.shape[0], M.shape[1])
    Minv[:3, :3] = R.transpose()
    Minv[:3, 3] = -R.transpose().dot(T)
    return Minv

def getIntrinsics(calib_cam):
    # Check if the calibration includes the rectification
    if calib_cam.P is not None:
        # P[:3] is the intrinsic matrix that also includes the rectifying rotation
        return calib_cam.P[:3, :3]
    else:
        # Just return K
        return calib_cam.K

def getExtrinsics(calib_cam):
    R = calib_cam.R
    T = calib_cam.T
    # Check if the calibration includes the rectification
    if calib_cam.Rrect is not None:
        Q = calib_cam.Rrect
        R = Q.dot(R)
        T = Q.dot(T)
    RT = np.eye(4)
    RT[:3, :3] = R
    RT[:3, 3] = T.reshape(3)
    return RT

def undistortRectify(img, calib_cam):
    # Get calibration parameters
    K = calib_cam.K
    D = calib_cam.D
    width = calib_cam.resolution[0]
    height = calib_cam.resolution[1]
    if calib_cam.P is not None:
        P = calib_cam.P
        Rrect = calib_cam.Rrect
        rectify_flag = 1
    else:
        P = K
        Rrect = None
        rectify_flag = 0

    # Compute undistortion map and apply it to image
    mapx, mapy = cv2.initUndistortRectifyMap(K, D, Rrect, P, (width, height), 5)
    imgund = cv2.remap(img, mapx, mapy, cv2.INTER_LANCZOS4)
    return (imgund, rectify_flag)

def drawCheckerboard(img, K, R, T, nx=10, ny=8, sx=20, sy=20):
    pts2d = []
    size = 8 if img.shape[0] > 500 else 3
    for yy in range(ny):
        for xx in range(nx):
            p3d = np.asarray([xx * sx, yy * sy, 0]).reshape(3, -1)
            p3dcam = R.dot(p3d) + T
            p2dh = K.dot(p3dcam) / p3dcam[2]
            p2d = tuple(np.asarray(p2dh[:2], dtype=int))
            pts2d.append(p2d)
            cv2.circle(img, p2d, size, (255, 0, 0), 2)
    size = 2 if img.shape[0] > 500 else 1
    for i in range(ny):
        cv2.line(img, pts2d[i * nx], pts2d[(i + 1) * nx - 1], (255, 20, 20), size)
    for i in range(nx):
        cv2.line(img, pts2d[i], pts2d[(ny - 1) * nx + i], (255, 20, 20), size)
    return img

def printMat(m):
    print 'rows: %d' % m.shape[0]
    print 'cols: %d' % (m.shape[1] if len(m.shape) > 1 else 1)
    print 'dt: d'
    print 'data: [%s]' % ', '.join([str(v) for v in m.flatten()])


if __name__ == '__main__':
    n = 7
    if n ==7:
        calib = xmlparser.parse('/Data/13_calibration/ext_plane/test_ext_plane/extrinsics2.xml')
        RT1 = createRT(xmlparser.get(calib, ['camera_calibrations', 'camera_1', 'R']), xmlparser.get(calib, ['camera_calibrations', 'camera_1', 'T']))
        RT2 = createRT(xmlparser.get(calib, ['camera_calibrations', 'camera_2', 'R']), xmlparser.get(calib, ['camera_calibrations', 'camera_2', 'T']))
        print RT2.dot(invRT(RT1))
    elif n == 6:
        calib1 = SensorCalib('/Data/0_Dataset/multicam/bin/calib_out_s1c1_s2c2_40.yml')
        calib2 = SensorCalib('/Data/0_Dataset/multicam_out/calib_s2.yml')
        RT1 = getExtrinsics(calib1.camera_calib[1])
        RT2 = getExtrinsics(calib2.camera_calib[1])

        print('\ndx')
        printMat(RT1[:3, :3])
        printMat(RT1[:3, 3])

        print('\nsx')
        printMat(RT2[:3, :3])
        printMat(RT2[:3, 3])

        print('\ndiff')
        RT = invRT(RT2).dot(RT1)
        printMat(RT[:3, :3])
        printMat(RT[:3, 3])
    elif n == 5:
        calib = SensorCalib('/Users/giulio/Dropbox (Personal)/Temporary/multicam/calib_s1_small_s2_s3_s4_rect.yml', 1)
        RT1 = getExtrinsics(calib.camera_calib[1])
        RT2 = getExtrinsics(calib.camera_calib[2])
        RT = RT2.dot(invRT(RT1))[:3, :]
        printMat(RT)
        printMat(invRT(RT))
    elif n == 4:
        calib = SensorCalib('/Users/giulio/Dropbox (Personal)/Temporary/multicam/calib_s1_small_s2_s3_s4_rect.yml', 1)
        for calib_idx in calib.camera_calib:
            calib_cam = calib.camera_calib[calib_idx]
            RT = getExtrinsics(calib_cam)[:3, :]
            print '\ncam %d' % calib_idx
            printMat(RT)
            printMat(invRT(RT))
    elif n == 3:
        calib = SensorCalib('/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4_rect.yml')
        calib.write('/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4_rect.yml')
    elif n == 2:
        calib = SensorCalib('/Data/0_Dataset/multicam_out/calib_s1.yml')
        calib.camera_calib[0].scale(0.5)
        calib.camera_calib[1].scale(0.5)
        calib.write('/Data/0_Dataset/multicam_out/calib_s1_small.yml')
    elif n == 1:
        calib = ymlparser.parse('/Data/0_Dataset/multicam_out/calib_s1.yml')
        calib['camera_calibrations']['camera_0']['K'][:2, :] *= 0.5
        calib['camera_calibrations']['camera_0']['rectified_P'][:2, :] *= 0.5
        calib['camera_calibrations']['camera_0']['resolution'][0] *= 0.5
        calib['camera_calibrations']['camera_0']['resolution'][1] *= 0.5
        calib['camera_calibrations']['camera_1']['K'][:2, :] *= 0.5
        calib['camera_calibrations']['camera_1']['rectified_P'][:2, :] *= 0.5
        calib['camera_calibrations']['camera_1']['resolution'][0] *= 0.5
        calib['camera_calibrations']['camera_1']['resolution'][1] *= 0.5
        ymlparser.write('/Data/0_Dataset/multicam_out/calib_s1_small.yml', calib)
    elif n == 0:
        calib = SensorCalib('/Users/giulio/git/sampledata/calib.yml')
        print calib
