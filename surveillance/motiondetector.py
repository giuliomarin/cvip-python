import sys
import os
import argparse
import datetime
from cvip import utils
import time
import numpy as np
import cv2

outDir = '/Users/giulio/Desktop/surveillance'
if not os.path.exists(outDir):
    os.makedirs(outDir)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--minarea", type=int, default=500, help="minimum area size")
ap.add_argument("-w", "--weightnew", type=float, default=0.05, help="weight new frame background")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(2)
    for i in range(5):
        camera.read()

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])

# Background model
background = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    text = "Good"

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = utils.resizeimgw(frame, 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the background is None, initialize it
    if background is None:
        background = gray
        continue
    background = (args['weightnew'] * gray + (1 - args['weightnew']) * background).astype(np.uint8)

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(background, gray)
    thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=5)
    _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    moving = False
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["minarea"]:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Moving"
        if not moving:
            moving = True
            frameorig = frame.copy()

    # draw the text and timestamp on the frame
    cv2.putText(frame, 'Status: %s' % text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if moving
    cv2.imshow("Security Feed", frame)
    img = np.concatenate((thresh, frameDelta))
    cv2.imshow("Thresh | Frame delta", img)
    if moving:
        filepath = os.path.join(outDir, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.jpg'))
        cv2.imwrite(filepath, frameorig)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
