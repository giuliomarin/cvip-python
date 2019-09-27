import numpy
import transformations
import xmlparser as xml
import numpy as np
import calibration.utils as ut

def saveplyNorm(filename, data, binary=True):
    with open(filename, 'w') as fid:
        # header
        fid.write('ply\n')
        if binary:
            fid.write('format binary_little_endian 1.0\n')
        else:
            fid.write('format ascii 1.0\n')
        fid.write('element vertex %d\n' % data.shape[0])
        fid.write('property float x\n')
        fid.write('property float y\n')
        fid.write('property float z\n')
        if data.shape[1] == 6:
            fid.write('property float nx\n')
            fid.write('property float ny\n')
            fid.write('property float nz\n')
        fid.write('end_header\n')

    # data
    if binary:
        fid = open(filename, 'ab')
        np.float32(data).tofile(fid)
    else:
        with open(filename, 'a') as fid:
            if data.shape[1] == 3:
                for p in data:
                    fid.write('%f %f %f\n' % tuple(p))
            elif data.shape[1] == 6:
                for p in data:
                    fid.write('%f %f %f %f %f %f\n' % tuple(p))

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


def generatePlane_old(a, b, c, d, t=[0, 0, 0], sx=1000, sy=1000, n=100):
    # generate parallel plane
    numpy.meshgrid()
    xx = numpy.linspace(-sx / 2, sx / 2, n) + sx / 2
    yy = numpy.linspace(-sy / 2, sy / 2, n) + sy / 4
    x, y = numpy.meshgrid(xx, yy)
    z = (-a*x - b*y - d) / c
    xyz = numpy.concatenate([x.reshape(-1, 1), y.reshape(-1, 1), z.reshape(-1, 1)], axis = 1)
    return xyz

    # rotate
    angle = numpy.arccos(numpy.dot([0, 0, 1], [a, b, c]))
    dirRot = numpy.cross([0, 0, 1], [a, b, c])
    R = numpy.eye(3)
    if numpy.linalg.norm(dirRot) > 0:
        R = transformations.rotation_matrix(angle, dirRot)[0:3, 0:3]
    xyz = xyz.dot(R)

    # translate
    dist = d / numpy.sqrt(a * a + b * b + c * c)
    t += dist * numpy.asarray([a, b, c])
    xyz += numpy.full(xyz.shape, t)
    return xyz

def generatePlane(R, T, sx=1000, sy=1000, n=100):
    # generate parallel plane
    numpy.meshgrid()
    xx = numpy.linspace(-sx/2, sx/2, n) + sx/2
    yy = numpy.linspace(-sy/2, sy/2, n) + sy/4
    x, y = numpy.meshgrid(xx, yy)
    z = x * 0
    xyz = numpy.concatenate([x.reshape(1, -1), y.reshape(1, -1), z.reshape(1, -1)], axis = 0)
    nxyz = numpy.repeat(numpy.asarray([0.0, 0.0, 1.0]).reshape(3, 1), [xyz.shape[1]], axis=1)

    # apply RT
    xyz = R.dot(xyz) + T
    nxyz = R.dot(nxyz)
    plane = numpy.concatenate([xyz.transpose(), nxyz.transpose()], axis=1)
    return plane

def generateLine(p, s=100):
    # generate points
    numpy.meshgrid()
    xx = numpy.linspace(0, p[0], s)
    yy = numpy.linspace(0, p[1], s)
    zz = numpy.linspace(0, p[2], s)
    xyz = numpy.concatenate([xx.reshape(1, -1), yy.reshape(1, -1), zz.reshape(1, -1)], axis = 0)
    return xyz.transpose()


def addColor(data, color):
    if data.shape[0] == numpy.asmatrix(color).shape[0]:
        data = numpy.concatenate([data, numpy.asarray(color, dtype=numpy.float32)], axis=1)
    else:
        # all the points with the same color
        data = numpy.concatenate([data, numpy.full(data.shape, color, dtype=numpy.float32)], axis=1)
    return data

if __name__ == '__main__':
    # saveply('/Data/1_seat/calibration/static/ProcessedCalib/linefit2.ply', generateLine([ 0.62455576  ,223.36923498  ,  4.3469712]))
    # exit(0)
    # R0 = transformations.rotation_matrix(np.deg2rad(90), [0, 1, 0])[:3, :3]
    # R2 = transformations.rotation_matrix(np.deg2rad(0), [0, 0, 1])[:3, :3]
    # R = R1.dot(R2)
    # T0 = np.asarray([0, 0, 400]).reshape(3, 1)
    # RT = ut.invRT(ut.createRT(R0, T0))
    # R = RT[:3, :3]
    # T = RT[:3, 3]
    # print R[0,0], R[0,1], R[0,2], R[1,0], R[1,1], R[1,2], R[2,0], R[2,1], R[2,2]
    # print T.reshape(1, -1)[0]
    # exit(0)
    # calibfile = '/Users/giulio/git/build/Nitrogen/bin/RelWithDebInfo/calibprocessor_output/ProcessedCalib/groundPlane2_0.xml'
    # R = xml.get(xml.parse(calibfile), ['R'])
    # T = xml.get(xml.parse(calibfile), ['T'])
    R = np.eye(3, 3)
    T = np.zeros((3, 1))
    T[2] = -10
    # xyz = generatePlane(R, T, sx=3000, sy=2000, n=200)
    xyz1 = generatePlane_old(-0.1739757247656447, -0.1471357140530122, 0.9736958091942161, -1712.2660981218, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    xyz2 = generatePlane_old(-0.00685339135623694, 0.01196929453942089, 0.9999048789835695, -1763.609602353019, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    xyz3 = generatePlane_old(0.03785034863688105, 0.03479222609448789, 0.9986775516208706, -1772.628191766928, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    xyz4 = generatePlane_old(0.3757807079842011, 0.2069417789909105, -0.9033072343422086, 1734.297230004126, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    xyz5 = generatePlane_old(0.09728790942495205, 0.05028039690834277, -0.9755710774267763, 1699.70217477357, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    xyz6 = generatePlane_old(0.09910161573522477, 0.05121775771396297, -0.9937583262813056, 1731.389160116277, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    # xyz = generatePlane_old(-3.0907468865760481e-02, 8.6710145662411597e-01, -4.9717179353685026e-01, 4.4008037031715230e+02, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    # xyz = generatePlane_old(0., 0., -1., 500, t=[0, 0, 0], sx=3000, sy=5000, n=200)
    saveplyNorm('/data/8_sizing/topdown/tmp/p1.ply', xyz1)
    saveplyNorm('/data/8_sizing/topdown/tmp/p2.ply', xyz2)
    saveplyNorm('/data/8_sizing/topdown/tmp/p3.ply', xyz3)
    saveplyNorm('/data/8_sizing/topdown/tmp/p4.ply', xyz4)
    saveplyNorm('/data/8_sizing/topdown/tmp/p5.ply', xyz5)
    saveplyNorm('/data/8_sizing/topdown/tmp/p6.ply', xyz6)
