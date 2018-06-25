"""
Giulio Marin
2018/06/05

Utilities to load, get, modify and write xml files
"""

#########
# Imports
#########

import numpy
from xml.etree import ElementTree

###########
# Functions
###########

def get(node, elements = None):
    if elements:
        for e in elements:
            node = node.find(e)

    # Add more cases
    if node.get('type_id') != 'opencv-matrix':
        return node.text.strip()
    r = int(node.find('rows').text)
    c = int(node.find('cols').text)
    txt = node.find('data').text.split()
    return numpy.array([float(x) for x in txt]).reshape((r, c))


def set(node, elements, element):
    pathToNode = elements[:-1]
    if len(pathToNode) > 0:
        for e in elements:
            node = node.find(e)

    # Check if node has to be added
    if node.find(elements[-1]) is None:
        newNode = ElementTree.SubElement(node.getroot(), elements[-1])
        if type(element) is numpy.ndarray:
            newNode.set("type_id", "opencv-matrix")
            ElementTree.SubElement(newNode, 'rows')
            ElementTree.SubElement(newNode, 'cols')
            ElementTree.SubElement(newNode, 'data')

    # update new node
    newNode = node.find(elements[-1])
    if type(element) is not numpy.ndarray:
        newNode.text = str(element)
    else:
        newNode.set("type_id", "opencv-matrix")
        rows = newNode.find('rows')
        rows.text = str(element.shape[0])
        cols = newNode.find('cols')
        cols.text = str(element.shape[1])
        data = newNode.find('data')
        data.text = '\n' + '\n'.join(' '.join(str(cell) for cell in row) for row in element)

    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    indent(newNode)
    return node


def parse(filepath):
    return ElementTree.parse(filepath)


def write(node, filename):
    node.write(filename)
    content = open(filename, "r").read()
    fid = open(filename, "wb")
    fid.write('<?xml version="1.0"?>\n')
    fid.write(content)
    fid.close()


###########
# Test
###########


if __name__ == '__main__':
    calib = parse('/media/data/cache/build/bin/front/ProcessedCalib/extrinsics2.xml')
    print get(calib, ['camera_calibrations', 'camera_0', 'K'])
