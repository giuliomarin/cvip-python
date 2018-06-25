import numpy as np
from matplotlib import pyplot as plt

#################
# Variables
#################

TARGET_SIZE_MM = 200.
CAM_RESOLUTION = 1280 * 2
CAM_FOCAL = 1040. * 2

#################
# Functions
#################

def rotMat(deg):
    rad = np.deg2rad(deg)
    return np.asmatrix([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])

#################
# Main
#################

if __name__ == "__main__":

    # projection matrix
    K = np.asmatrix([[CAM_FOCAL, CAM_RESOLUTION / 2], [0, 1]])

    #################
    # Fix distance and change angle
    #################

    dists = [500, 750, 1000, 1250, 1500]
    angles = np.arange(0, 90)
    lengths = []
    for dist in dists:
        length = []
        for angle in angles:
            # Target points after RT
            R = rotMat(angle)
            T = np.asmatrix([0, dist]).transpose()
            pt3d1 = R.dot(np.asmatrix([-TARGET_SIZE_MM / 2, 0]).transpose()) + T
            pt3d2 = R.dot(np.asmatrix([TARGET_SIZE_MM / 2, 0]).transpose()) + T

            # Project points
            pt2d1 = float((K.dot(pt3d1) / pt3d1[-1])[:-1])
            pt2d2 = float((K.dot(pt3d2) / pt3d2[-1])[:-1])
            l = np.abs(pt2d1 - pt2d2)
            length.append(l)
            print "[d: %-6.1f, a: %-4.1f] pts: [%-6.1f, %-6.1f] length: %-6.1f px" % (dist, angle, pt2d1, pt2d2, l)
        lengths.append(length)

    # Plot
    plt.figure()
    plt.title("TargetSize: %.1f mm - CamRes: %d px - CamFocal: %.1f px" % (TARGET_SIZE_MM, CAM_RESOLUTION, CAM_FOCAL))
    for l in lengths:
        plt.plot(angles, np.gradient(l, angles))
    plt.legend(["d: %.0f mm" % d for d in dists], loc="lower left")
    plt.grid()
    plt.ylabel("grad size projected target [px/deg]")
    plt.xlabel("angle [deg]")

    #################
    # Fix angle and change distance
    #################

    angles = [0, 15, 30, 45, 60]
    dists = np.arange(500, 1500)
    lengths = []
    for angle in angles:
        length = []
        for dist in dists:
            # Target points after RT
            R = rotMat(angle)
            T = np.asmatrix([0, dist]).transpose()
            pt3d1 = R.dot(np.asmatrix([-TARGET_SIZE_MM / 2, 0]).transpose()) + T
            pt3d2 = R.dot(np.asmatrix([TARGET_SIZE_MM / 2, 0]).transpose()) + T

            # Project points
            pt2d1 = float((K.dot(pt3d1) / pt3d1[-1])[:-1])
            pt2d2 = float((K.dot(pt3d2) / pt3d2[-1])[:-1])
            l = np.abs(pt2d1 - pt2d2)
            length.append(l)
            print "[d: %-6.1f, a: %-4.1f] pts: [%-6.1f, %-6.1f] length: %-6.1f px" % (dist, angle, pt2d1, pt2d2, l)
        lengths.append(length)

    # Plot
    plt.figure()
    plt.title("TargetSize: %.1f mm - CamRes: %d px - CamFocal: %.1f px" % (TARGET_SIZE_MM, CAM_RESOLUTION, CAM_FOCAL))
    for l in lengths:
        plt.plot(dists, np.gradient(l, dists))
    plt.legend(["a: %.0f deg" % d for d in angles], loc="lower right")
    plt.grid()
    plt.ylabel("grad size projected target [px/mm]")
    plt.xlabel("distance [mm]")
    plt.show()