import numpy
import transformations
import xmlparser as xml
import numpy as np
import calibration.utils as ut


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
    xx = numpy.linspace(-sx / 2., sx / 2., n)
    yy = numpy.linspace(-sy / 2., sy / 2., n)
    x, y = numpy.meshgrid(xx, yy)
    z = x * 0
    xyz = numpy.concatenate([x.reshape(-1, 1), y.reshape(-1, 1), z.reshape(-1, 1)], axis = 1)

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
    xx = numpy.linspace(-sx/2, sx/2, n)
    yy = numpy.linspace(-1000, sy, n)
    x, y = numpy.meshgrid(xx, yy)
    z = x * 0
    xyz = numpy.concatenate([x.reshape(1, -1), y.reshape(1, -1), z.reshape(1, -1)], axis = 0)

    # apply RT
    xyz = R.dot(xyz) + T
    return xyz.transpose()

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
    R0 = transformations.rotation_matrix(np.deg2rad(90), [0, 1, 0])[:3, :3]
    # R2 = transformations.rotation_matrix(np.deg2rad(0), [0, 0, 1])[:3, :3]
    # R = R1.dot(R2)
    T0 = np.asarray([0, 0, 400]).reshape(3, 1)
    RT = ut.invRT(ut.createRT(R0, T0))
    R = RT[:3, :3]
    T = RT[:3, 3]
    print R[0,0], R[0,1], R[0,2], R[1,0], R[1,1], R[1,2], R[2,0], R[2,1], R[2,2]
    print T.reshape(1, -1)[0]
    # exit(0)
    calibfile = '/Users/giulio/git/build/Nitrogen/bin/RelWithDebInfo/calibprocessor_output/ProcessedCalib/groundPlane2.xml'
    R = xml.get(xml.parse(calibfile), ['R'])
    T = xml.get(xml.parse(calibfile), ['T'])
    R = np.eye(3, 3)
    T = np.zeros((3, 1))
    xyz = generatePlane(R, T, sx=420, sy=2000)
    xyz = generatePlane(R, T, sx=420, sy=1000)
    # xyz = generatePlane(0, 0, 1, 500, sx=500, sy=1000)
    saveply('/Users/giulio/git/build/Nitrogen/bin/RelWithDebInfo/camerapositioningtool_output/line.ply', xyz)
