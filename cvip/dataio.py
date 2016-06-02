import cv2
import numpy as np


def imread(imgPath):
    """
    Load a char/float mat stored in a png file
        \param imgPath : path to the .png image
        \return : is float
        \return : matrix values
    """
    ## Read the png image
    img = cv2.imread(imgPath, -1)
    if img is None:
        raise IOError('File not found: %s' % imgPath)
    if img.shape[2] == 4:
        return imread32f(imgPath), 1
    else:
        return img, 0


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
    imFloat = np.zeros(imSize, np.float32)
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
                imggray = img.astype(np.uint8)
            else:
                imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if isinstance(colmap, np.ndarray):
                img = colmap[imggray] * 255
            else:
                img = colmap(imggray) * 255
        return cv2.imwrite(imgPath, img)


def imwrite32f(imgPath, img):
    """
    Write a float matrix in a png file
        \param imgPath : path to the .png image
        \img : image to store
    """
    # Check input
    if not (img.dtype == np.float32):
        raise TypeError('Image is not float32')
    # Save image
    imgToWrite = np.zeros((img.shape[0], img.shape[1], 4), np.uint8)
    imgToWrite.data = img.data
    cv2.imwrite(imgPath, imgToWrite)


if __name__ == '__main__':
    print 'done'