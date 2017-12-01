import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from cvip import *
from calibration import utils as calib_utils


class TestCalib(unittest.TestCase):
    def test_createRT(self):
        R = np.eye(3)
        Rbad = np.eye(2)
        T = [0, 0, 0]
        Tbad = [0, 0]
        RT = calib_utils.createRT(R, T)
        self.assertEquals(RT.shape, (4, 4))
        self.assertRaises(ValueError, calib_utils.createRT, Rbad, T)
        self.assertRaises(ValueError, calib_utils.createRT, R, Tbad)

    def test_invRT(self):
        R = np.eye(3)
        T = np.asarray([1, 0, 0])
        RT = calib_utils.createRT(R, T)
        RTinv_real = calib_utils.createRT(R, -T)
        RTinv = calib_utils.invRT(RT)
        self.assertEquals(RTinv.shape, RT.shape)
        self.assertEqual(np.linalg.norm(RTinv - RTinv_real), 0.)
        RTbad = np.eye(3)
        self.assertRaises(ValueError, calib_utils.invRT, RTbad)
        RTbad = np.eye(4, 3)
        self.assertRaises(ValueError, calib_utils.invRT, RTbad)


class TestDataIO(unittest.TestCase):
    def test_imread(self):
        img, type = dataio.imread('float.png')
        self.assertTrue(type == 1)
        img, type = dataio.imread('rgb.png')
        self.assertTrue(type == 0)
        self.assertRaises(TypeError, dataio.imread32f, 'rgb.png')

    def test_imwrite(self):
        img = np.random.random((10, 10)).astype(np.int)
        self.assertRaises(TypeError, dataio.imwrite32f, './tmp.png', img)

    def test_writeread(self):
        imgw = np.random.random((10, 10)).astype(np.float32)
        dataio.imwrite32f('./tmp.png', imgw)
        imgr = dataio.imread32f('./tmp.png')
        self.assertFalse(np.any(np.abs(imgw - imgr)))


class TestUtils(unittest.TestCase):
    def test_plotcam(self):
        fig = utils.plt.figure('camera')
        ax = utils.Axes3D(fig)
        r = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        utils.plotcam(ax, r, [10, 0, 0], col=[1, 0, 0], scale=0.5)

    def test_concatenateimages(self):
        pathimg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rgb.png')
        utils.mergeimages([pathimg, pathimg], 2, 0.5, './merge.png')
        img, _ = dataio.imread(pathimg)
        imgmerge, _ = dataio.imread('./merge.png')
        self.assertTrue(imgmerge.shape[1] == img.shape[1])


if __name__ == '__main__':
    unittest.main()
