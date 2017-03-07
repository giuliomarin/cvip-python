import sys
import cv2
import time

# Input
imgName = sys.argv[1] if len(sys.argv) > 1 else 'img'
scale = int(sys.argv[2]) if len(sys.argv) == 3 else 1

# Open camera
cap = cv2.VideoCapture(0)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w / scale)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h / scale)

# Acquire some frame to adjust exposure
for i in range(4):
    ret, frame = cap.read()
    time.sleep(0.5)

# Save image
imgPath = '%s.png' % imgName
print 'Saving %s' % imgPath
cv2.imwrite(imgPath, frame)

# Close camera
cap.release()
