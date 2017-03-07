import numpy as np
import re
from cvip import pointcloud as pc

if __name__ == "__main__":
    if False:
        with open('/Users/giulio/Library/Logs/Aquifi/log.txt') as fid:
            lines = fid.readlines()
            for l in lines:
                l = l.strip()
                if 'Centroids x:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        xvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        xvec = []
                elif 'Centroids y:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        yvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        yvec = []
                elif 'Centroids z:' in l:
                    matchObj = re.match(r'.*\[(.*)\].*', l, re.M | re.I)
                    if len(matchObj.group(1)) > 0:
                        zvec = np.array(matchObj.group(1).split(','), dtype = float)
                    else:
                        zvec = []
    else:
        xvec = [-982, 837]
        yvec = [-469, 1010]
        zvec = [926, 2706]
    tz = np.mean(zvec)
    data = []
    for d in xvec:
        data.append(pc.addColor(pc.generatePlane(1, 0, 0, d, [0, 0, tz]), color))
    if len(data) > 0:
        data = np.concatenate(data)
        pc.saveply('/Users/giulio/Desktop/x.ply', data)
    data = []
    for d in yvec:
        data.append(pc.addColor(pc.generatePlane(0, 1, 0, d, [0, 0, tz]), [0, 255, 0]))
    if len(data) > 0:
        data = np.concatenate(data)
        pc.saveply('/Users/giulio/Desktop/y.ply', data)
    data = []
    for d in zvec:
        data.append(pc.addColor(pc.generatePlane(0, 0, 1, d), [0, 0, 255]))
    if len(data) > 0:
        data = np.concatenate(data)
        pc.saveply('/Users/giulio/Desktop/z.ply', data)