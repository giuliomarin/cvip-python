import sys
import os
import cv2
from cvip import dataio
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def showimages(img1, img2, pathtosave):

    # if len(img1.shape) < 3 or img1.shape[2] < 3:
    #     img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    # if len(img2.shape) < 3 or img2.shape[2] < 3:
    #     img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    def press(event):
        sys.stdout.flush()
        if event.key == 'escape':
            sys.exit(0)
        elif event.key == ' ':
            plt.savefig(os.path.join(pathtosave, 'overlay.pdf'), bbox_inches='tight')
            print 'saved'

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    plt.subplots_adjust(0.15, 0.1, 0.9, 0.98)

    im = ax.imshow(img1)

    axcolor = 'lightgoldenrodyellow'
    BAR_HEIGHT = 0.03
    axalpha = plt.axes([0.2, 0.2 * BAR_HEIGHT, 0.7, BAR_HEIGHT])#, facecolor=axcolor)
    # axmax = plt.axes([0.2, BAR_HEIGHT + 0.4 * BAR_HEIGHT, 0.7, BAR_HEIGHT], axisbg = axcolor)
    salpha = Slider(axalpha, 'Alpha', 0.0, 1.0, valinit=1.0)

    def update(event):
        curralpha = salpha.val
        ax.clear()
        ax.imshow(img1, alpha=curralpha)
        ax.imshow(img2, alpha=(1 - curralpha))
        plt.draw()
        return curralpha
    salpha.on_changed(update)

    plt.show()


if __name__ == '__main__':
    img1 = dataio.opencv2matplotlib(dataio.imread('/GitHub/sampledata/stereo/left.png')[0])
    img2 = dataio.opencv2matplotlib(dataio.imread('/GitHub/sampledata/stereo/disp.png')[0])
    print img1.shape

    showimages(img1, img2, '.')