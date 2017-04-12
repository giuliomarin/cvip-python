import numpy
from xml.etree import ElementTree

# Usage: node = parse(filepath)
def getmat(node, elements = []):
    if len(elements) > 0:
        for e in elements:
            node = node.find(e)

    # Add more cases
    if node.get('type_id') != 'opencv-matrix':
        return node.text
    r = int(node.find('rows').text)
    c = int(node.find('cols').text)
    txt = node.find('data').text.split()
    return numpy.array([float(x) for x in txt]).reshape((r, c))

def parse(filepath):
    return ElementTree.parse(filepath)
