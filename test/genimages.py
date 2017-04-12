import numpy as np
import time
import cv2
while 1:
    img = np.random.rand(200, 200) * 255
    cv2.imwrite("/GitHub/giuliomarin.github.io/extra/test.png", img)
    time.sleep(1)