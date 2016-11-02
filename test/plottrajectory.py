from cvip import ymlparser
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
import os
import ntpath

def setaxis(ax):
    if (minx > 0) & (maxx > 0) & (miny > 0) & (maxy > 0) & (minz > 0) & (maxz > 0):
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)
        ax.set_zlim(minz, maxz)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

mainfolderpath = '/Volumes/Builds/JenkinsBuilds/NitrogenNew/master_manual/1319_36ef7e30ef6a9b23cf1bdf17f84b5c16ca73286a/ScanningRegressionTest_linux'

videolistpath = os.path.join(mainfolderpath, 'videolist.txt')
videolist = []
if not os.path.exists('results'):
    os.mkdir('results')
with open(videolistpath, 'r') as fileid:
    filecontent = fileid.readlines()
    for line in filecontent:
        videoname = ntpath.basename(line.rstrip())
        videolist.append(videoname)

fig = plt.figure('trajectory')
for currvideo in videolist:
    print 'Processing video: %s' % currvideo
    folderpath = os.path.join(mainfolderpath, currvideo, 'scanlive')
    filecontent = ymlparser.parse(folderpath + '/trajectory.yml')
    ntransf = ymlparser.parse(folderpath + '/viewInfo.yml')['nTransf']
    ntransf = np.linalg.inv(np.asmatrix(ntransf))


    tvecx = []
    tvecy = []
    tvecz = []
    for idx in range(filecontent['numViews']):
        t = filecontent['view_calibrations']['view_%d' % idx]['tvec']
        tvecx.append(t[0][0])
        tvecy.append(t[1][0])
        tvecz.append(t[2][0])
    #
    # fig = plt.figure()
    # ax = fig.gcaticklabels(projection = '3d')
    # ax.plot(np.asarray(tvecx), np.asarray(tvecy), np.asarray(tvecz))
    # plt.savefig('./test.pdf')

    if (len(tvecx) == 0) | (len(tvecy) == 0) | (len(tvecz) == 0):
        tvecx = [0]
        tvecy = [0]
        tvecz = [0]

    tvecx = np.asmatrix(tvecx).transpose()
    tvecy = np.asmatrix(tvecy).transpose()
    tvecz = np.asmatrix(tvecz).transpose()
    tvec1 = np.asmatrix([1] * len(tvecx)).transpose()

    vec = np.concatenate([tvecx, tvecy, tvecz, tvec1], axis = 1)
    # vecrot = vec.dot(ntransf)

    minx = np.min(vec[:, 0]) * 0.9
    maxx = np.max(vec[:, 0]) * 0.9
    miny = np.min(vec[:, 1]) * 0.9
    maxy = np.max(vec[:, 1]) * 0.9
    minz = np.min(vec[:, 2]) * 0.9
    maxz = np.max(vec[:, 2]) * 0.9

    ax = fig.add_subplot(2, 2, 1, projection = '3d')
    ax.plot(np.asarray(vec[:,0].transpose())[0], np.asarray(vec[:,1].transpose())[0], np.asarray(vec[:,2].transpose())[0], '-b.')
    ax.set_aspect('equal')
    setaxis(ax)
    ax.view_init(30, 0)
    ax = fig.add_subplot(2, 2, 2, projection = '3d')
    ax.plot(np.asarray(vec[:,0].transpose())[0], np.asarray(vec[:,1].transpose())[0], np.asarray(vec[:,2].transpose())[0], '-b.')
    ax.set_aspect('equal')
    setaxis(ax)
    ax.view_init(30, 90)
    ax = fig.add_subplot(2, 2, 3, projection = '3d')
    ax.plot(np.asarray(vec[:,0].transpose())[0], np.asarray(vec[:,1].transpose())[0], np.asarray(vec[:,2].transpose())[0], '-b.')
    ax.set_aspect('equal')
    setaxis(ax)
    ax.view_init(30, 180)
    ax = fig.add_subplot(2, 2, 4, projection = '3d')
    ax.plot(np.asarray(vec[:,0].transpose())[0], np.asarray(vec[:,1].transpose())[0], np.asarray(vec[:,2].transpose())[0], '-b.')
    ax.set_aspect('equal')
    setaxis(ax)
    ax.view_init(30, 270)
    # ax.plot(np.asarray(vecrot[:,0].transpose())[0], np.asarray(vecrot[:,1].transpose())[0], np.asarray(vecrot[:,2].transpose())[0], 'r')

    plt.tight_layout()
    plt.savefig('./results/%s.png' % currvideo, transparent = True)
    plt.clf()
    # plt.show()
