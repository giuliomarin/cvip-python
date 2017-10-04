labelpathin = '/Data/1_seat/label.csv'
labelpathout = '/Data/1_seat/labels.csv'

HEADER = 4
HEADER_DEFECT = 5

fin = open(labelpathin, 'r')
fout = open(labelpathout, 'w')

# headers
line = fin.readline()
l = line.strip().split(',')
fout.write(','.join(l[:HEADER + HEADER_DEFECT]) + '\n')

# entries
lines = fin.readlines()
for line in lines:
    l = line.strip().split(',')
    numdefects = len(l[HEADER:]) / HEADER_DEFECT
    if numdefects == 0:
        fout.write(','.join(l[:HEADER]) + ','.join(['-'] * (HEADER_DEFECT + 1)) + '\n')
    else:
        for i in range(numdefects):
            fout.write(','.join(l[:HEADER]) + ',' + ','.join(l[HEADER + HEADER_DEFECT*i:HEADER + HEADER_DEFECT + HEADER_DEFECT*i]) + '\n')

# close files
fin.close()
fout.close()