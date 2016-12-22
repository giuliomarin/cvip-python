import numpy as np
import re
from cvip import transformations as tf

def saveply(filename, data):
    with open(filename, 'w') as fid:
        # header
        fid.write('ply\n')
        fid.write('format ascii 1.0\n')
        fid.write('element vertex %d\n' % data.shape[0])
        fid.write('property float x\n')
        fid.write('property float y\n')
        fid.write('property float z\n')
        if data.shape[1] == 6:
            fid.write('property uchar red\n')
            fid.write('property uchar green\n')
            fid.write('property uchar blue\n')
        fid.write('end_header\n')

        # data
        if data.shape[1] == 3:
            for p in data:
                fid.write('%f %f %f\n' % tuple(p))
        elif data.shape[1] == 6:
            for p in data:
                fid.write('%f %f %f %.0f %.0f %.0f\n' % tuple(p))

def generatePlane(a, b, c, d, t = [0, 0, 0], s = 1000, n = 100):
    # generate parallel plane
    np.meshgrid()
    xx = np.linspace(-s, s, n)
    yy = np.linspace(-s, s, n)
    x, y = np.meshgrid(xx, yy)
    z = x * 0
    xyz = np.concatenate([x.reshape(-1, 1), y.reshape(-1, 1), z.reshape(-1, 1)], axis = 1)

    # rotate
    angle = np.arccos(np.dot([0, 0, 1], [a, b, c]))
    dirRot = np.cross([0, 0, 1], [a, b, c])
    R = np.eye(3)
    if np.linalg.norm(dirRot) > 0:
        R = tf.rotation_matrix(angle, dirRot)[0:3, 0:3]
    xyz = xyz.dot(R)

    # translate
    dist = d / np.sqrt(a * a + b * b + c * c)
    t += dist * np.asarray([a, b, c])
    xyz += np.full(xyz.shape, t)
    return xyz

def addColor(data, color):
    if data.shape[0] == np.asmatrix(color).shape[0]:
        data = np.concatenate([data, np.asarray(color, dtype=np.float32)], axis=1)
    else:
        # all the points with the same color
        data = np.concatenate([data, np.full(data.shape, color, dtype=np.float32)], axis=1)
    return data

if __name__ == "__main__":
    if False:
        with open('/Users/giulio/Library/Logs/Aquifi/log.txt') as fid:
            lines = fid.readlines()
            for l in lines:
                l = l.strip()
                if 'Centroids x:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        xvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        xvec = []
                elif 'Centroids y:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        yvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        yvec = []
                elif 'Centroids z:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        zvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        zvec = []
    else:
        xvec = [-982, 837]
        yvec = [-469, 1010]
        zvec = [926, 2706]
    tz = np.mean(zvec)
    data = []
    for d in xvec:
        data.append(addColor(generatePlane(1, 0, 0, d, [0, 0, tz]), color))
    if len(data) > 0:
        data = np.concatenate(data)
        saveply('/Users/giulio/Desktop/x.ply', data)
    data = []
    for d in yvec:
        data.append(addColor(generatePlane(0, 1, 0, d, [0, 0, tz]), [0, 255, 0]))
    if len(data) > 0:
        data = np.concatenate(data)
        saveply('/Users/giulio/Desktop/y.ply', data)
    data = []
    for d in zvec:
        data.append(addColor(generatePlane(0, 0, 1, d), [0, 0, 255]))
    if len(data) > 0:
        data = np.concatenate(data)
        saveply('/Users/giulio/Desktop/z.ply', data)