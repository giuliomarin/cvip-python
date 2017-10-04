from scipy.misc import imread, imsave
from sklearn.cluster import KMeans
import numpy as np
from subprocess import call
import os

def computeDescriptor(img):
    # patch size
    X = 20
    Y = 20

    # number of patches
    nX = img.shape[1] / X
    nY = img.shape[0] / Y

    descriptor = []
    for x in range(nX):
        for y in range(nY):
            val = np.mean(img[x * X:(x + 1) * X, y * Y:(y + 1) * Y, :])
            descriptor.append(val)
    return np.asmatrix(descriptor)

def computeDescriptors(imgs):
    descriptors = []
    for img in imgs:
        descriptor = computeDescriptor(img)
        if len(descriptors) == 0:
            descriptors = descriptor
        else:
            descriptors = np.append(descriptors, descriptor, axis=0)

    descriptors_mean = np.mean(descriptors, axis=0)
    descriptors_std = np.std(descriptors - descriptors_mean, axis=0)
    descriptors_norm = (descriptors - descriptors_mean) / descriptors_std
    descriptors = {'vals': descriptors_norm, 'mean': descriptors_mean, 'std': descriptors_std}
    return descriptors

def computeDistance(descriptors, query):
    dist = np.linalg.norm(descriptors - query, axis=1)
    ids = range(descriptors.shape[0])
    ids_sort = sorted(ids, key=lambda k: dist[k])
    dist_sort = sorted(dist)
    return ids_sort, dist_sort

if __name__ == '__main__':
    # parameters
    imglist = '/Users/giulio/Desktop/validation/listPatchTot.txt'
    outpath = '/Users/giulio/Desktop/class'
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # compute descripts
    imgs = []
    for imgpath in open(imglist, 'r').readlines():
        img = imread(imgpath.strip())
        imgs.append(img)
    descriptors = computeDescriptors(imgs)

    # cluster descriptors
    nclusters = 20
    if True:
        kmeans = KMeans(n_clusters=nclusters).fit(descriptors['vals'])
        labels = kmeans.labels_
        with open(outpath + '/labels.txt', 'w') as fid:
            for v in labels:
                fid.write('%d\n' % v)
    else:
        with open(outpath + '/labels.txt', 'r') as fid:
            labels = [int(v) for v in fid.readline().split()]

    classes = [[] for i in range(nclusters)]
    numImgs = [0 for i in range(nclusters)]
    for i, img in enumerate(imgs):
        img = np.asarray(img, np.float32)
        idx = labels[i]
        classes[idx] = img if len(classes[idx]) == 0 else classes[idx] + img
        numImgs[idx] = 1 if numImgs[idx] == 0 else numImgs[idx] + 1

    montagesrc = outpath + '/all'
    with open(montagesrc + '.txt', 'w') as fid:
        for i, img in enumerate(classes):
            img = img - np.min(img)
            img = img / np.max(img) * 255.0
            img = np.asarray(img, np.uint8)
            imgpath = outpath + '/class_%d.png' % i
            imsave(imgpath, img)
            fid.write('%s %d\n' % (imgpath, numImgs[i]))

    cmd = '$(cat ' + montagesrc + '.txt | sort -nrk2,2 | awk \'BEGIN{printf("montage ")} {printf("-label %d %s ", $2, $1)} END {printf("-geometry +1+1 ' + montagesrc + '.png' + '")}\')'
    call(cmd, shell=True)

    # # classify image
    # img = imread('/Data/1_seat/renderings/2017_03_23_13_19_38-back-chunk00_idx03.png')
    # img_descriptor = (computeDescriptor(img) - descriptors['mean']) / descriptors['std']
    # ids, dist = computeDistance(descriptors['vals'], img_descriptor)
    # print 'class: %d [%.3f]' % (ids[0], dist[0])