import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import transformations as tf
import numpy as np
import dataio
import cv2
import os


def plotcam(ax, r, t, col = [0.2, 0.2, 0.2], scale = 1.0, h = 3.0, w = 4.0, f = 7.0):
    """
        Plot a camera with a given pose. Camera looks at z.
            \param ax : handle to the axes
            \param r: orientation
            \param t: position
            \param col: color of the camera
            \param scale: size of the camera
    """

    pp = np.array([[0, 0, 0], [w/2, -h/2, f], [w/2, h/2, f], [-w/2, h/2, f], [-w/2, -h/2, f]]).transpose()
    pp *= scale
    pw = np.asarray(r).dot(pp) + np.asmatrix(t).transpose()
    pw = pw.transpose().tolist()

    for i in [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1]]:
        poly = Poly3DCollection([[pw[i[0]], pw[i[1]], pw[i[2]]]])
        poly.set_alpha(0.1)
        poly.set_color(col)
        ax.add_collection3d(poly)

    poly = Poly3DCollection([[pw[1], pw[2], pw[3], pw[4]]])
    poly.set_alpha(0.2)
    poly.set_color(col)
    ax.add_collection3d(poly)
    coloredaxes = np.asarray([pw[4], pw[1]])
    ax.plot(coloredaxes[:, 0], coloredaxes[:, 1], coloredaxes[:, 2], 'r', linewidth=2.0)  # x
    coloredaxes = np.asarray([pw[4], pw[3]])
    ax.plot(coloredaxes[:, 0], coloredaxes[:, 1], coloredaxes[:, 2], 'g', linewidth=2.0)  # y

def plotplane(ax, r, t, col = [0.2, 0.2, 0.2], scale = 1.0, h = 3.0, w = 4.0, f = 7.0):
    """
        Plot a camera with a given pose. Camera looks at z.
            \param ax : handle to the axes
            \param r: orientation
            \param t: position
            \param col: color of the camera
            \param scale: size of the camera
    """

    pp = np.array([[0, 0, 0], [w, 0, f], [w, h, f], [0, h, f], [0, 0, f]]).transpose()
    pp *= scale
    pw = np.asarray(r).dot(pp) + np.asmatrix(t).transpose()
    pw = pw.transpose().tolist()

    # for i in [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1]]:
    #     poly = Poly3DCollection([[pw[i[0]], pw[i[1]], pw[i[2]]]])
    #     poly.set_alpha(0.1)
    #     poly.set_color(col)
    #     ax.add_collection3d(poly)

    poly = Poly3DCollection([[pw[1], pw[2], pw[3], pw[4]]])
    poly.set_alpha(0.2)
    poly.set_color(col)
    ax.add_collection3d(poly)
    coloredaxes = np.asarray([pw[4], pw[1]])
    ax.plot(coloredaxes[:, 0], coloredaxes[:, 1], coloredaxes[:, 2], 'r', linewidth=2.0)  # x
    coloredaxes = np.asarray([pw[4], pw[3]])
    ax.plot(coloredaxes[:, 0], coloredaxes[:, 1], coloredaxes[:, 2], 'g', linewidth=2.0)  # y


def mergeimages(imagesList, numCols, resize = 1.0, nameOut = None):
    """
        Create image concatenating the input images.
            \param imagesList : list of paths to images
            \param numCols: number of images to concatenate horizontally (<0 makes one row)
            \param resize: resize factor of the final image
            \param nameOut: path to the image to save
            \preturn: the images concatenated
    """

    # Check if images have to be concatenated horizontally
    horizontal = 0
    if numCols < 0:
        numCols = len(imagesList)
        horizontal = 1

    g_imgRows = g_imgCols = g_imgChannels = 0;
    imgNum = 0
    for imageName in imagesList:
        try:
            img, _ = dataio.imread(imageName)
        except:
            print 'Image not valid: %s' % imageName
            continue
        if img is None:
            continue
        imgshape = img.shape
        if len(imgshape) > 2:
            imgRows, imgCols, imgChannels = imgshape
        else:
            imgChannels = 1
            imgRows, imgCols = imgshape

        # Assign global values
        if imgNum == 0:
            imgNum += 1
            g_imgRows = imgRows
            g_imgCols = imgCols
            g_imgChannels = imgChannels
            imgMergeRow = img
            imgType = os.path.splitext(imageName)[1]
        else:
            # Discard images with different size
            if (imgRows != g_imgRows) | (imgCols != g_imgCols) | (imgChannels != g_imgChannels):
                print 'Skipped image: %s' % imageName
                continue

            imgNum = imgNum + 1
            if numCols == 1:
                imgMergeRow = np.concatenate((imgMergeRow, img))
                imgMerge = imgMergeRow
            elif imgNum % numCols == 0:
                imgMergeRow = np.concatenate((imgMergeRow, img), axis = 1)
                if imgNum == numCols:
                    imgMerge = imgMergeRow
                else:
                    imgMerge = np.concatenate((imgMerge, imgMergeRow))
            elif (imgNum - 1) % numCols == 0:
                imgMergeRow = img
            else:
                imgMergeRow = np.concatenate((imgMergeRow, img), axis = 1)

        print 'Added file: %s' % imageName

    # Check if last row is not full
    if imgMergeRow.shape[1] != numCols * g_imgCols:
        if horizontal == 0:
            imgMergeRow = np.concatenate((imgMergeRow, np.zeros(
                (g_imgRows, numCols * g_imgCols - imgMergeRow.shape[1], imgMergeRow.shape[2]), np.uint8)), axis = 1)
        if 'imgMerge' in locals():
            imgMerge = np.concatenate((imgMerge, imgMergeRow))
        else:
            imgMerge = imgMergeRow

    # Resize image
    if resize != 1:
        imgMerge = cv2.resize(imgMerge, (0, 0), fx = resize, fy = resize)

    # Save imageName
    if nameOut:
        cv2.imwrite(nameOut, imgMerge)
        print("Done: " + nameOut)
    return imgMerge


def cropimage(img, tlbr):

    # TODO: handle different roi input and grayscale images
    tl = tlbr[0]
    br = tlbr[1]
    img_crop = img[tl[0]:br[0], tl[1]:br[1], :]
    return img_crop


def alignimage(ref, img):
    # Convert images to grayscale
    if (len(ref.shape) > 2) & (ref.shape[2] == 3):
        im1_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    else:
        im1_gray = ref
    if (len(img.shape) > 2) & (img.shape[2] == 3):
        im2_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        im2_gray = img

    # Find size of image1
    sz = ref.shape

    # Define the motion model
    warp_mode = cv2.MOTION_HOMOGRAPHY

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype = np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype = np.float32)

    # Specify the number of iterations.
    number_of_iterations = 100

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-6

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC(im1_gray, im2_gray, warp_matrix, warp_mode, criteria)

    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        # Use warpPerspective for Homography
        im2_aligned = cv2.warpPerspective(img, warp_matrix, (sz[1], sz[0]),
                                          flags = cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else:
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(img, warp_matrix, (sz[1], sz[0]), flags = cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    # TODO: handle exception if function does not converge

    return im2_aligned

def resizeimgh(img, h):
    if h <= 0:
        return img
    else:
        return cv2.resize(img, (int(float(img.shape[1]) / img.shape[0] * h), h))


def resizeimgw(img, w):
    if w <= 0:
        return img
    else:
        return cv2.resize(img, (w, int(float(img.shape[0]) / img.shape[1] * w)))


def tostr(arr, prec = 3):
    strout = ''
    for l in arr:
        for c in l:
            strout += ('%.' + str(prec) + 'f ') % c
        strout += '\n'
    return strout

if __name__ == '__main__':

    # Test merge images
    if False:
        # imagesList = [f for f in os.listdir(imgsFolder) if
        #               os.path.isfile(os.path.join(imgsFolder, f))]  # and f[0] == 'd'
        # def _natural_sort_key(s):
        #     return [int(text) if text.isdigit() else text.lower() for text in re.split(re.compile('([0-9]+)'), s)]
        # imagesList.sort(key = _natural_sort_key)

        mergeimages(['../unittests/rgb.png', '../unittests/rgb.png'], 2, 0.2, '../unittests/merge.png')

    # Test plot camera
    if True:
        fig = plt.figure('camera')
        ax = Axes3D(fig)

        # plot camera 1
        r = tf.rotation_matrix(np.deg2rad(0), [0, 0, 1])[:3, :3]
        plotcam(ax, r, [0, 0, 0], scale=0.05)

        # plot camera 2
        r = tf.rotation_matrix(np.deg2rad(90), [1, 0, 0])[:3, :3]
        plotcam(ax, r, [1, 0, 0], col=[0.2, 0.2, 0.2], scale=0.05)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim((-1, 1))
        ax.set_ylim((-1, 1))
        ax.set_zlim((-1, 1))
        ax.autoscale_view()
        plt.show()
