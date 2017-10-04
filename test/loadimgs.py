import os
import numpy as np
from matplotlib import pyplot as plt

a = []
a.append(np.asarray(plt.imread('/Data/1_seat/2017_02_22_22_58_22/back/renderDefectsLocO/chunk00_idx00_D0.png') * 255, np.uint8))
a.append(np.asarray(plt.imread('/Data/1_seat/2017_02_22_22_58_22/back/renderDefectsLocO/chunk00_idx01_D0.png') * 255, np.uint8))

b = []
with open('/Data/1_seat/2017_02_22_22_58_22/back/renderDefectsLoc/patches.bin', 'rb') as f:
    fsize = os.fstat(f.fileno()).st_size
    while f.tell() < fsize:
        b.append(np.fromfile(f, np.uint8, 224*224*3).reshape([224, 224, 3])[:, :, ::-1])


print a[0][222,216], a[1][222,216]
print b[0][222,216], b[1][222,216]

plt.figure()
plt.imshow(a[0])
plt.figure()
plt.imshow(a[1])
plt.figure()
plt.imshow(b[0])
plt.figure()
plt.imshow(b[1])
plt.show()