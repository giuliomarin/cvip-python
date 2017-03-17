import numpy
import transformations


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


def generatePlane(a, b, c, d, t=[0, 0, 0], s=1000, n=100):
    # generate parallel plane
    numpy.meshgrid()
    xx = numpy.linspace(-s, s, n)
    yy = numpy.linspace(-s, s, n)
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


def addColor(data, color):
    if data.shape[0] == numpy.asmatrix(color).shape[0]:
        data = numpy.concatenate([data, numpy.asarray(color, dtype=numpy.float32)], axis=1)
    else:
        # all the points with the same color
        data = numpy.concatenate([data, numpy.full(data.shape, color, dtype=numpy.float32)], axis=1)
    return data