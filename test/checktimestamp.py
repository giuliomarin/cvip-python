import numpy as np
import struct
from cvip import dataio

def getTimestamp(img):
    str = ''
    for i in range(8):
        str = format(img[0, i], '08b') + str
    n = np.uint64(0)
    for p, s in enumerate(reversed(str)):
        if s == '1':
            s2 = np.uint64(1)
            for j in range(p):
                s2 *= np.uint64(2)
            n += s2
    return n

def getTimestampDiff(t1, t2):
    if t1 > t2:
        return np.int(t1 - t2)
    else:
        return -np.int(t2 - t1)

ts = []
seqs = [
'/Data/14_metal/dearborn/2018_10_01_18_58_21_a copy/side0/sirs/sir0/Frames/master_1.png',
'/Data/14_metal/dearborn/2018_10_01_18_58_21_a copy/side1/sirs/sir0/Frames/master_1.png'
]
for seq in seqs:
    img = dataio.imread(seq)[0]
    t = getTimestamp(img)
    print t
    ts.append(np.uint64(t))

for i in range(1, len(ts)):
    if ts[i] > ts[i-1]:
        print np.int(ts[i] - ts[i-1])
    else:
        print -np.int(ts[i - 1] - ts[i])
