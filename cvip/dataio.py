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


def imread(imgPath, alpha=True):
    """
    Load a char/float mat stored in a png file
        \param imgPath : path to the .png image
        \return : matrix values
        \return : is float
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
        img = numpy.asarray(cv2.imread(imgPath, -1))

        if (img.ndim > 2) and (img.shape[2] == 4):
            if alpha:
                # float
                return imread32f(imgPath), 1
            else:
                img = img[:, :, :3]
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

    print('Writing: %s' % imgPath)
    if img.dtype == numpy.float32:
        return imwrite32f(imgPath, img)
    else:
        if colmap is not None:
            if len(img.shape) < 3:
                imggray = img.astype(numpy.uint8)
            else:
                imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if isinstance(colmap, numpy.ndarray):
                img = colmap[imggray] * 255
            else:
                img = colmap(imggray) * 255
        return cv2.imwrite(imgPath, opencv2matplotlib(img))

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
    imgToWrite.data = img.flatten()
    cv2.imwrite(imgPath, imgToWrite)


if __name__ == '__main__':
    import sys
    img = imread(sys.argv[1])[0]
    # img = imread(sys.argv[1])[0]
    # imgorig = img.copy()
    # img[img <= 0] = numpy.nan
    # img[img > 1500] = numpy.nan
    # d = numpy.mean(img[~numpy.isnan(img)])
    # print d
    # img = 1/img * 600 * 50
    # img1 = imread('/GitHub/build/Nitrogen/bin/RelWithDebInfo/19/sir/Prefilter/slavePre_1.png')[0]
    # img2 = imread('/GitHub/CommonTools/submodules/Nitrogen/30/sir/Prefilter/slavePre_1.png')[0]
    # img1 = imread('/GitHub/build/Nitrogen/bin/RelWithDebInfo/Snapshot23_1thread/sir/Prefilter/masterPre_1.png')[0]
    # img2 = imread('/GitHub/build/Nitrogen/bin/RelWithDebInfo/Snapshot23/sir/Prefilter/masterPre_1.png')[0]

    # cmin = d * 0.97
    # cmax = d * 1.03
    # img[(d - 1 < imgorig) & (imgorig < d + 1)] = numpy.nan
    # img[cmax < imgorig] = numpy.nan
    # img[cmin > imgorig] = numpy.nan
    # img[0,0] = cmin
    # img[0,1] = cmax
    # img = numpy.abs(img1.astype(float) - img2.astype(float))
    # print numpy.sum(img)
    # img = imread('/GitHub/build/Nitrogen/bin/RelWithDebInfo/31/sir/Disparity/disparity_1.png')[0]
    # img = imread('/GitHub/build/Nitrogen/bin/RelWithDebInfo/Snapshot17/sir/Disparity/disparity_2.png')[0]
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.colorbar()
    # plt.title('Distance: %d' % d)
    # plt.colorbar()
    # plt.imsave("disp1.png", img, cmap='Greys')
    plt.show()
