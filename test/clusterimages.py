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
    # dist = np.linalg.norm(descriptors - query, axis=1)
    dist = np.max(descriptors - query, axis=1)
    ids = range(descriptors.shape[0])
    ids_sort = sorted(ids, key=lambda k: dist[k])
    dist_sort = sorted(dist)
    return ids_sort, dist_sort


if __name__ == '__main__':
    # parameters
    nclusters = 1
    train = True
    imglist = '/Users/giulio/git/script/html/showimgs/listClean.txt'
    imgtest = '/Users/giulio/git/script/html/showimgs/listTest.txt'
    outpath = '/Users/giulio/Desktop/cluster/c9_4cam_20171004/s4_p42_v0_c113'
    imglist = outpath + '/listClean.txt'
    imgtest = outpath + '/listTest.txt'
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # compute descripts
    imgs = []
    for imgpath in open(imglist, 'r').readlines():
        img = imread(imgpath.strip())
        imgs.append(img)
    descriptors = computeDescriptors(imgs)

    # cluster descriptors
    if train:
        kmeans = KMeans(n_clusters=nclusters).fit(descriptors['vals'])
        labels = kmeans.labels_
        with open(outpath + '/labels.txt', 'w') as fid:
            for v in labels:
                fid.write('%d\n' % v)
        centers = kmeans.cluster_centers_
        # centers = np.mean(descriptors['vals'], axis=0)
        np.save(outpath + '/centers.npy', centers)

        classes = [[] for i in range(nclusters)]
        numImgs = [0 for i in range(nclusters)]
        for i, img in enumerate(imgs):
            img = np.asarray(img, np.float32)
            idx = labels[i]
            classes[idx] = img if len(classes[idx]) == 0 else classes[idx] + img
            numImgs[idx] = numImgs[idx] + 1

        montagesrc = outpath + '/all'
        with open(montagesrc + '.txt', 'w') as fid:
            for i, img in enumerate(classes):
                img = img - np.min(img)
                img = img / np.max(img) * 255.0
                img = np.asarray(img, np.uint8)
                imgpath = outpath + '/class_%d.png' % i
                imsave(imgpath, img)
                fid.write('%s %d\n' % (imgpath, numImgs[i]))
                # fid.write('%s\n' % imgpath)

        # cmd = '$(cat ' + montagesrc + '.txt | sort -nrk2,2 | awk \'BEGIN{printf("montage ")} {printf("-label %d %s ", $2, $1)} END {printf("-geometry +1+1 ' + montagesrc + '.png' + '")}\')'
        # call(cmd, shell=True)

    # classify images
    res = []
    with open(outpath + '/labels.txt', 'r') as fid:
        labels = [int(v) for v in fid.readlines()]
    centers = np.load(outpath + '/centers.npy')
    for imgpath_gt in open(imgtest, 'r').readlines():
        imgpath = imgpath_gt.split()[0]
        gt = int(imgpath_gt.split()[1])
        img = imread(imgpath)
        img_descriptor = (computeDescriptor(img) - descriptors['mean']) / descriptors['std']
        ids, dist = computeDistance(centers, img_descriptor)
        # ids, dist = computeDistance(descriptors['vals'], img_descriptor)
        res.append((gt, dist[0]))
        # print 'class: %d gt: %d dist: %.3f' % (labels[ids[0]], gt, dist[0])

    # res.sort(key=lambda x: x[1])
    with open(outpath + '/res.txt', 'w') as fid:
        for r in res:
            print 'gt: %d dist: %.3f' % (r[0], r[1])
            fid.write('gt: %d dist: %.3f\n' % (r[0], r[1]))