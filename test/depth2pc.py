import sys
import numpy as np
from cvip import pointcloud as pc
from cvip import dataio as io

if __name__ == '__main__':
    # read image
    imgpath = sys.argv[1] if len(sys.argv) > 1 else '/GitHub/build/Nitrogen/bin/Debug/Snapshot1/sir/Disparity/disparity_1.png'
    # imgpath = sys.argv[1] if len(sys.argv) > 1 else '/Data/aqp75/2/sir/Disparity/disparity_1.png'
    img = io.imread(imgpath)[0]

    # create calib
    w = img.shape[1]; h = img.shape[0]
    fx = 600; fy = 600; cx = w / 2; cy = h / 2
    K = np.asarray([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    Ki = np.linalg.inv(K)

    # create list of points
    uu, vv = np.meshgrid(range(w), range(h))
    u = uu.reshape(1, -1)[0]
    v = vv.reshape(1, -1)[0]
    z = img.reshape(1, -1)[0]
    zgood = z > 10
    z[~zgood] = 1.
    z = 50 * fx / z
    uvz = np.stack((u * z, v * z, z), axis=0)
    uvz = np.compress(zgood, uvz, axis=1)
    print uvz.shape
    xyz = Ki.dot(uvz)

    # save point cloud
    pc.saveply('disp.ply', pc.addColor(xyz.transpose(), [0, 0, 255]))
