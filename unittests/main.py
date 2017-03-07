import unittest
import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from cvip import *


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
        utils.plotcam(ax, r, [10, 0, 0], col = [1, 0, 0], scale = 0.5)

    def test_concatenateimages(self):
        pathimg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rgb.png')
        utils.mergeimages([pathimg, pathimg], 2, 0.5, './merge.png')
        img, _ = dataio.imread(pathimg)
        imgmerge, _ = dataio.imread('./merge.png')
        self.assertTrue(imgmerge.shape[1] == img.shape[1])

if __name__ == '__main__':
    unittest.main()