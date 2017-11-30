'''
Parse YML file

Giulio Marin
giulio.marin@me.com

2016/6/11
'''

import numpy as np
from collections import OrderedDict
from pyaml import *

###########################################################
# Constant
###########################################################

# YML header
YML_HEADER = '%YAML:'


###########################################################
# Functions
###########################################################

def prepareStringForReading(ymlFilePath):
    """
    load the yaml file into a string, ready for reading using the yaml library 
        \param ymlFilePath, path to the yml file to parse
        \return strToRead, string to read
    """

    # Add opencv yaml constructor
    yaml.add_constructor(u"tag:yaml.org,2002:opencv-matrix", ndarrayConstructor)
    yaml.add_constructor(u"tag:yaml.org,2002:ndarray", ndarrayConstructor)

    # read the file in lines
    lines = readLines(ymlFilePath)
        
    # remove the header if it's YAML
    if lines[0].startswith(YML_HEADER) or lines[0].startswith(YML_HEADER.lower()):
        lines.pop(0)

    # join into a unique string
    strToRead = '\n'.join(lines)
    
    # replace all the quotes adding the escape \ first:
    escape = "\\"
    quote = "\""
    strToRead = strToRead.replace(quote, escape + quote)

    return strToRead


def checkFile(ymlFilePath):
    """
    check if a file is yaml parsable
        \param ymlFilePath, path to the yml file to parse
        \return true or false, result of the check
    """
    # try to parse the file
    try:
        yamlObj = parse(ymlFilePath)
        success = True
    except Exception, e:
        print('Failed to parse yaml file.\nError: ' + str(e))
        success = False

    # return
    return success


def parse(ymlFilePath):
    """
    parse the file
        \param ymlFilePath, path to the yml file to parse
        \return ymlObj, object of the parsed file
    """
    # prepare string for reading
    strToRead = prepareStringForReading(ymlFilePath)

    # try to parse the file
    try:  
        yamlObj = yaml.load(strToRead)
        success = True
    except Exception, e:
        raise Exception('Failed to parse yaml file.\nError: ' + str(e))

    # return
    return yamlObj


def getInfoFromNodePath(ymlFilePath, nodePath):
    """
    get the value of a given yml path of nodes
        \param ymlFilePath, path to the yml file to parse
        \param nodePath, list of nodes (from the root to the node that we want to read)
    """
    ymlObj = parse(ymlFilePath)
    return getInfoFromNode(ymlObj, nodePath)

def getInfoFromNode(ymlObj, nodePath):
    """
        \param ymlFilePath,  yml object
        \param nodePath, list of nodes (from the root to the node that we want to read)
    """
    # get the string value from the field selected
    try:
        # go through the other nodes in the path
        for nodeName in (nodePath):
            try:
                ymlObj = ymlObj[nodeName]
            except:
                raise Exception('Failed to get node ' + nodeName)

        # if here we got to the end of the path
        value = ymlObj
        return value

    except Exception, err:
        raise Exception('Cannot get to the end of path ' + str(nodePath) + ' in file ' + ymlFilePath + '\nError found: ' + str(err.message))


def checkNodeExists(ymlObj, nodePath):
    """
    check if a node exists
        \param ymlObj, yml object
        \param nodePath, list of nodes (from the root to the node that we want to check)
    """
    # just try to read the node
    try:
        _ = getInfoFromNode(ymlObj, nodePath)
        return True
    except Exception:
        return False


def write(ymlFilePath, ymlObj, header=None):

    """
    write to file a yml obj
        \param ymlFilePath, path to the yml file to parse
        \param ymlObj, object containing the yml info
        \param header, header line to be written to the yml file
    """ 
    
    # create a stream to write to file
    stream = file(ymlFilePath, 'w')

    # dump the yml content into the stream
    yaml.add_representer(np.ndarray, ndarrayRepresenter)
    represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)
    yaml.dump(ymlObj, stream)
    stream.close()

    # correct the '-' in the file (they are always 2 spaces behind)
    lines = readLines(ymlFilePath)
    document = '\n'.join(lines)

    # correct the '\'' in the file (they do not need to be read and python add them to every string)
    # document = document.replace('\'', '')

    # eliminate the escape \ for the quotes in the final document
    escape = "\\"
    quote = "\"" 
    document = document.replace(escape + quote, quote)

    if header :
        document = YML_HEADER + '1.0\n' + document

    # re-write the file
    with open(ymlFilePath, 'w') as outfile:
        outfile.write(document)   


def readLines(filename):
    """
Read lines as in a txt file
    \param filename path to the txt file to read
    \return thisList list of lines 
"""
    # check if the file exist
    if not os.path.exists(filename):
        raise Exception("file", filename, "not found")

    # read the file
    with open(filename, 'r') as file:
        thisList = [row.split('\n', 1)[0] for row in file]
    return thisList


def ndarrayConstructor(loader, node):
    """
    Define an YAML constructor for loading from a YAML node 
    (YAML to Python Numpy Array)
        \param loader: loader, instance of pyYaml
        \param node: node to het the data from
    """

    mapping = loader.construct_mapping(node, deep=True)
    mat = np.array(mapping["data"])
    mat.resize(mapping["rows"], mapping["cols"])

    # Return matrix
    return mat

 
def ndarrayRepresenter(dumper, mat):
    """
    Define a YAML representer for dumping into a YAML node
    (Python Numpy Array to YAML opencv matrix like representation)
        \param dumper: loader instance of PyYaml
        \param mat: matrice to dump
    """

    if len(mat.shape) == 1:
        rows = 1
        cols = mat.shape[0]
    else:
        rows = mat.shape[0]
        cols = mat.shape[1]
    mapping = OrderedDict()
    mapping['rows'] = rows
    mapping['cols'] = cols
    mapping['dt'] = 'd'
    mapping['data'] = mat.reshape(-1).tolist()
    return dumper.represent_mapping(u"tag:yaml.org,2002:ndarray", mapping)


#########################################################
# main for debugging purposes only module
#########################################################

if __name__ == "__main__":
    pass