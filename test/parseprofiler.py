import os
import numpy as np

def profiler2csv(profilerpath, idtokeep):
    entries = []
    with open(profilerpath, 'r') as fid:
        tokeep = False
        for line in fid.readlines():
            l = line.strip()

            # First valid entry
            if not tokeep and l.startswith('name '):
                tokeep = True
                continue

            # Last valid entry
            if tokeep and l.startswith('-------'):
                break

            # Save entry (avg, name, id, idp)
            fields = l.split('|')
            # debug: print "[%6.1f] %s" % (float(fields[2]) / 1000., fields[0].strip())
            entries.append((float(fields[2]) / 1000., fields[0].strip(), int(fields[1].strip()), int(fields[-1].strip())))

    # Sort given id
    entries.sort(key=lambda x: x[2])

    # Create csv
    header = ''
    body = ''
    for e in entries:
        # Save only main pipelines modules
        if e[2] in idtokeep:
            header += '%s,' % e[1]
            body += '%.1f,' % e[0]

    # Print sorted entries
    if 0:
        entriessort = sorted(entries, key=lambda x: -x[0])
        print "\nSorted entries:"
        for e in entriessort: print "[%5.1f] %s" % (e[0], e[1])

    # return
    return header, body

if __name__ == '__main__':

    idtokeep = [31, 32, 33, 34, 35, 42, 507, 690]

    # all builds
    if 1:
        mainpath = '/Volumes/Builds/JenkinsBuilds/NitrogenNew/master'

        profileraverage = []
        profilerbuild = []
        head = []
        # for all the builds
        for d in sorted(os.listdir(mainpath)):  #, reverse=True):
            bodies = []
            headers = []
            buildpath = os.path.join(mainpath, d, 'ScanningRegressionTest_linux_AARCH64')
            if not os.path.isdir(buildpath):
                continue
            print 'Processing build: %s' % buildpath,
            # for all the videos
            isvalid = 0
            for v in sorted(os.listdir(buildpath)):
                profilerpath = os.path.join(buildpath, v, 'profiler.txt')
                if not os.path.exists(profilerpath):
                    continue
                header, body = profiler2csv(profilerpath, idtokeep)
                if len(header.split(',')) - 1 != len(idtokeep):
                    continue
                isvalid = 1
                header = 'video,%s' % header
                body = '%s,%s' % (v, body)
                headers.append(header)
                bodies.append(body)
            if isvalid:
                print ' [valid]'
                allentries = []
                for b in bodies:
                    allentries.append([float(v) for v in b.split(',')[1:-1]])
                profileraverage.append(np.mean(np.asarray(allentries), axis=0))
                profilerbuild.append(d)
                head = headers
            else:
                print ' [skip]'

        if len(head) > 0:
            # save to file
            with open('profiler.csv', 'w') as fid:
                fid.write('build')
                for h in head[0].split(',')[1:-1]:
                    fid.write(',%s' % h)
                fid.write('\n')
                for i, p in enumerate(profileraverage):
                    fid.write('%s' % profilerbuild[i])
                    for v in p:
                        fid.write(',%.3f' % v)
                    fid.write('\n')

            # save plot
            from matplotlib import pyplot as plt
            plt.clf()
            plt.plot(profileraverage)
            plt.grid()
            plt.draw()
            plt.ylim((0, 200))
            plt.legend(head[0].split(',')[1:-1], loc='upper left', fontsize=10)
            plt.pause(0.001)
            plt.savefig('profiler.pdf')

    # single file
    if 0:
        profilerpath = '/Volumes/Builds/JenkinsBuilds/NitrogenNew/master/3675_f05726f1f43cb42320f7e2456ea2508604e4e382/ScanningRegressionTest_linux_AARCH64/ScanGT_sir30C_Whale1_u001/profiler.txt'
        outcsvpath = 'profiler.csv'
        header, body = profiler2csv(profilerpath, idtokeep)
        with open(outcsvpath, 'w') as fid:
            fid.write(header[:-1] + '\n')
            fid.write(body[:-1])
