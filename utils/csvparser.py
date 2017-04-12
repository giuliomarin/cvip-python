import numpy as np

if __name__ == '__main__':
    filename = '/Users/giulio/Downloads/kinect_leap_dataset/acquisitions/P4/G7/2_leap_motion.csv'
    data = dict()
    with open(filename, 'r') as fid:
        lines = fid.readlines()
        for line in lines:
            vals = line.strip().split(',')
            data[vals[0]] = vals[1:]
    xyz = np.array(data['FingertipsPositions']).astype(np.float).reshape((3, -1)).transpose()
    print xyz