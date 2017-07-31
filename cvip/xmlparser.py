import numpy
from xml.etree import ElementTree

# Usage: node = parse(filepath)
def get(node, elements = []):
    if len(elements) > 0:
        for e in elements:
            node = node.find(e)

    # Add more cases
    if node.get('type_id') != 'opencv-matrix':
        return node.text.strip()
    r = int(node.find('rows').text)
    c = int(node.find('cols').text)
    txt = node.find('data').text.split()
    return numpy.array([float(x) for x in txt]).reshape((r, c))

def parse(filepath):
    return ElementTree.parse(filepath)

if __name__ == '__main__':
    calib = parse('/Data/1_seat/originaldata/2017_03_22_14_26_12/front/ProcessedCalib/extrinsics0_simple.xml')
    print get(calib, ['camera_calibrations', 'camera_0', 'K'])
