import cv2
import numpy
import array
import os

def opencv2matplotlib(img):
    """
    Invert channels if input image has 3 channels
    :param img: input image
    :return: image converted
    """
    if (img.ndim > 2) and (img.shape[2] == 3):
        return img[:, :, ::-1]
    else:
        return img


def imread(imgPath):
    """
    Load a char/float mat stored in a png file
        \param imgPath : path to the .png image
        \return : is float
        \return : matrix values
    """

    # Check if file exists
    if not os.path.exists(imgPath):
        raise IOError('File not found: %s' % imgPath)

    # Read image
    if imgPath.endswith('pfm'):
        # pfm image
        img = imreadpfm(imgPath)
        return img, 1
    else:
        # png image
        img = cv2.imread(imgPath, -1)

        if (img.ndim > 2) and (img.shape[2] == 4):
            # float
            return imread32f(imgPath), 1
        else:
            # char
            return opencv2matplotlib(img), 0


def imreadpfm(imgPath):
    """
    Load a float mat stored in a pfm file
        \param imgPath : path to the .pfm image
        \return : matrix values
    """
    with open(imgPath) as fid:
        line = fid.readline()
        colsrows = fid.readline().split()
        cols = int(colsrows[0])
        rows = int(colsrows[1])
        scale = fid.readline()
        elem = array.array('f', fid.read()).tolist()
        img = numpy.rot90(numpy.asarray(elem, dtype = numpy.float32).reshape((cols, rows), order = 'F'))
        return img


def imread32f(imgPath):
    """
    Load a float mat stored in a png file
        \param imgPath : path to the .png image
        \return : matrix values
    """
    ## Read the png image
    img = cv2.imread(imgPath, -1)
    if img is None:
        raise IOError('File not found: %s' % imgPath)
    # Convert it to float
    imSize = (img.shape[0], img.shape[1])
    imFloat = numpy.zeros(imSize, numpy.float32)
    try:
        imFloat.data = img.data
    except:
        raise TypeError('Image is not float32: %s' % imgPath)

    return imFloat


def imwrite(imgPath, img, colmap = None):
    """
    Write a char/float mat to file
        \param imgPath : path to the .png image
        \img : image to store
    """
    if (len(img.shape) > 2) and (img.shape[2] == 4):
        return imwrite32f(imgPath, img)
    else:
        if not colmap is None:
            if len(img.shape) < 3:
                imggray = img.astype(numpy.uint8)
            else:
                imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if isinstance(colmap, numpy.ndarray):
                img = colmap[imggray] * 255
            else:
                img = colmap(imggray) * 255
        return cv2.imwrite(imgPath, img)

#TODO write function to save pfm format

def png2pgm(pathImgIn, minVal = 0, maxVal = 255):
    img, isfloat = imread(pathImgIn)

    img = numpy.asarray(img, numpy.float32)

    # Check input
    minVal = max(minVal, 0)
    minVal = float(minVal)
    maxVal = min(maxVal, 2 ** 16)
    maxVal = float(maxVal)

    img[img < 0] = 0

    # Scale
    img = img - minVal
    img = img / (maxVal - minVal)
    img = img * (2 ** 16)

    # Convert to int
    img = numpy.asarray(img, numpy.uint16)

    return img


def imwrite32f(imgPath, img):
    """
    Write a float matrix in a png file
        \param imgPath : path to the .png image
        \img : image to store
    """
    # Check input
    if not (img.dtype == numpy.float32):
        raise TypeError('Image is not float32')
    # Save image
    imgToWrite = numpy.zeros((img.shape[0], img.shape[1], 4), numpy.uint8)
    imgToWrite.data = img.data
    cv2.imwrite(imgPath, imgToWrite)


if __name__ == '__main__':
    import sys
    img = imread(sys.argv[1])[0]
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.colorbar()
    plt.show()
