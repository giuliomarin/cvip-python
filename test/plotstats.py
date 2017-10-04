import matplotlib.pyplot as plt

src = '/Users/giulio/Desktop/log.txt'
side = 'front'

side

for l in open(src, 'r').readlines():
    l = l.strip()
    if 'I-Results saved' in l and side in l:
        print l