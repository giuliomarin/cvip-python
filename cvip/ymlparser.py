'''
Parse YML file

Giulio Marin
giulio.marin@me.com

2016/6/11
'''

import numpy as np
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
    yaml.add_constructor(u"tag:yaml.org,2002:opencv-matrix", opencvMatrixConstructor)

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
    # get the string value from the field selected
    try:
        ymlObj = parse(ymlFilePath)
        
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


def checkNodeExists(ymlFilePath, nodePath):
    """
    check if a node exists
        \param ymlFilePath, path to the yml file to parse
        \param nodePath, list of nodes (from the root to the node that we want to check)
    """
    # just try to read the node
    try:
        nodeContent = getInfoFromNodePath(ymlFilePath, nodePath)
        return True
    except Exception:
        return False


def write(ymlFilePath, ymlObj, header = None):

    """
    write to file a yml obj
        \param ymlFilePath, path to the yml file to parse
        \param ymlObj, object containing the yml info
        \param header, header line to be written to the yml file
    """ 
    
    # create a stream to write to file
    stream = file(ymlFilePath, 'w')

    # dump the yml content into the stream
    dump(ymlObj, stream)
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


def replaceNodePathValue(ymlFilePath, nodePath, newValue, ymlFilePathOut = None):
    """
    get the list of subnodes names from a given node path
        \param ymlFilePath, path to the yml file to parse
        \param nodePath, list of nodes (from the root to the node that we want to read
        \param newValue, value to replace
    """ 

    # Check if file has to be replaced
    if ymlFilePathOut is None:
        ymlFilePathOut = ymlFilePath

    # check if a version header is present in the file
    firstLine = readLines(ymlFilePath)[0]

    # understand if the value to replace is a value or a vector
    if isinstance(newValue, list):
        # in case of a list first replace with an fake list of same dim (trick use string)
        replaceNodePathValue(ymlFilePath, nodePath, '[' + 'a,'*(len(newValue)-1) + 'a]', ymlFilePathOut)

        # then call recursively this function assigning every entry
        for entryId, entryNewValue in enumerate(newValue):
            nodePathEntry = nodePath + [entryId]
            replaceNodePathValue(ymlFilePathOut, nodePathEntry, entryNewValue)

    else:
        # get the string value from the field selected
        try:
            strValueToReplace = str(newValue)
            ymlObj = parse(ymlFilePath)

            # create a string to execute
            accessStr = ''
            for item in nodePath:
                accessStr = accessStr + '[' + repr(item) + ']'

            # evaluate if the field exists
            evalStr = 'ymlObj' + accessStr
            try:
                eval(evalStr)
            except:
                raise Exception('\nNode: ' + str(nodePath) + '\nnot found in: ' + ymlFilePath)

            # execute the replacement
            execStr = evalStr + ' = ' + '\'' + strValueToReplace + '\''
            exec(execStr)

            # write to file the object
            write(ymlFilePathOut, ymlObj)

            # if the original yaml file contained a version string, add it back at the top of the file
            if firstLine.startswith(YML_HEADER) or firstLine.startswith(YML_HEADER.lower()):
                doc = readLines(ymlFilePathOut)
                doc.insert(0, firstLine)
                with open(ymlFilePathOut, 'w') as outfile:
                    outfile.writelines(["%s\n" % item  for item in doc])
        except Exception, err:
            raise Exception('Cannot get to the end of path ' + str(nodePath) + ' in file ' + ymlFilePath + '\nError found: ' + str(err.message))


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


def opencvMatrixConstructor(loader, node):
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

 
def opencvMatrixRepresenter(dumper, mat):
    """
    Define a YAML representer for dumping into a YAML node
    (Python Numpy Array to YAML opencv matrix like representation)
        \param dumper: loader instance of PyYaml
        \param mat: matrice to dump
    """

    mapping = {'rows': mat.shape[0], 'cols': mat.shape[1], 'dt': 'd', 'data': mat.reshape(-1).tolist()}
    return dumper.represent_mapping(u"tag:yaml.org,2002:opencv-matrix", mapping)


def writeMatrix(yamlFilePath, node, value):
    """
    Write a single matrix in a yaml file at a given node
        \param yamlFilePath: path to the existing or to be created yaml file
        \param node: list of string to the node
        \param value: value to write at the node
    """

    # Check existence
    if os.path.exists(yamlFilePath):
        fileDidExist = True
    else:
        fileDidExist = False

    # Open file 
    f = open(yamlFilePath, 'a')

    # Add opencv yaml representer
    yaml.add_representer(np.ndarray, opencvMatrixRepresenter)

    # Write header if new file
    if not fileDidExist:
        f.write(YML_HEADER + " 1.0\n")

    # Convert node and value into a dictionary (stream)
    node.reverse()
    for subNodeIdx, subNode in enumerate(node):
        if subNodeIdx == 0:
            innestDict = {}
            innestDict[subNode] = value
            innerDicts = innestDict
        else:
            outterDict = {}
            outterDict[subNode] = innerDicts     
            innerDicts = outterDict
    stream = innerDicts
    
    # Dump data
    yaml.dump(stream, f)


def readMatrix(yamlFilePath, node, isThereHeader = True):
    """
    Read a opencv-like matrix from a yaml file 
        \param yamlFilePath: path to the existing or to be created yaml file
        \param node: node string list *** ONLY outter node supported (1 layer)***
        \param isThereHeader: (optional) is the file contain a header or not
        \retrun read matrix
    """
    
    # Check existence
    if not os.path.exists(yamlFilePath):
        raise Exception("File does not exist: " + yamlFilePath)
    
    # Add opencv yaml constructor 
    yaml.add_constructor(u"tag:yaml.org,2002:opencv-matrix", opencvMatrixConstructor)

     # Open file 
    f = open(yamlFilePath, 'r')
    if isThereHeader:
        header = f.readline()

    # Load
    rslt = yaml.load(f) 

    # Get the corresponding node
    return rslt[node[0]]


#########################################################
# main for debugging purposes only module
#########################################################

if __name__ == "__main__":

    if False:
        ymlFilePath = '/GitHub/Fusion/apps/computestereo/data/ParametersFile.yml'
        ymlFilePathOut = '/GitHub/Fusion/apps/computestereo/data/ParamsFile.yml'
        nodePath = ['global', 'min_disparity']
        newValue = 0
        replaceNodePathValue(ymlFilePath, nodePath, newValue, ymlFilePathOut)
        print 'Done'
        pass