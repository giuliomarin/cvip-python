from moviepy.editor import *
import os

# Create gif for Aquifi videos
if False:
    mainfolder = '/Users/giulio/Dropbox (Aquifi)/Data/ScanGtRegTestData/%s'
    for folder in os.listdir(mainfolder % ''):
        if os.path.isfile(mainfolder % folder):
            continue

        inPath = mainfolder % folder + '/Frames/%s'
        if not os.path.exists(inPath % ''):
            inPath = mainfolder % folder + '/sir/Frames/%s'
        imgpath = inPath % 'color0_%d.png'

        if os.path.exists(inPath % '../gif.gif'):
            continue

        nframes = len([name for name in os.listdir(inPath % '') if os.path.isfile(inPath % name) and name.startswith('color0')])
        imglist = range(1, nframes, int(nframes / 50.0))

        images = []
        for i in imglist:
            images.append(imgpath % i)

        clip = ImageSequenceClip(images, fps=15)
        # clip.crop(x1=400, x2=1100, y1=500, y2 = 1000)
        clip = clip.resize(1.0 / 6.0)
        clip.write_gif(inPath % '../gif.gif')