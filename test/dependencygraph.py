import os
import re
from collections import Counter

class Vertex:

    id_g = 0

    def __init__(self, node):
        self.id = Vertex.id_g
        Vertex.id_g += 1
        self.name = node
        self.adjacent = {}

    def __str__(self):
        return str(self.name) + ': ' + str([x.name for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        if node in self.vert_dict:
            return self.vert_dict[node]
        else:
            self.num_vertices = self.num_vertices + 1
            new_vertex = Vertex(node)
            self.vert_dict[node] = new_vertex
            return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def remove_vertex(self, n):
        if n not in self.vert_dict:
            return
        self.num_vertices -= 1
        del(self.vert_dict[n])

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        # self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def test(self):
        g = Graph()

        g.add_vertex('a')
        g.add_vertex('b')
        g.add_vertex('c')
        g.add_vertex('d')
        g.add_vertex('e')
        g.add_vertex('f')

        g.add_edge('a', 'b', 7)
        g.add_edge('a', 'c', 9)
        g.add_edge('a', 'f', 14)
        g.add_edge('b', 'c', 10)
        g.add_edge('b', 'd', 15)
        g.add_edge('c', 'd', 11)
        g.add_edge('c', 'f', 2)
        g.add_edge('d', 'e', 6)
        g.add_edge('e', 'f', 9)

        for v in g:
            for w in v.get_connections():
                print '( %s , %s, %3d)' % (v.id, w.id, v.get_weight(w))

        for v in g:
            print g.vert_dict[v.id]

def log(s, fid):
    print s
    fid.write(s + '\n')

if __name__ == '__main__':

    src = '/GitHub/CommonTools/submodules/Nitrogen/modules'
    modules = [m for m in os.listdir(src) if os.path.isdir(os.path.join(src, m))]
    g = Graph()
    for modulename in modules:
        g.add_vertex(modulename)

        currmodule = '%s/%s' % (src, modulename)
        print 'Module: %s' % currmodule

        hppfiles = []
        for root, dirs, files in os.walk(currmodule):
            for f in files:
                if f.endswith(".hpp"):
                    currfile = os.path.join(root, f)
                    hppfiles.append(currfile)

        setfiles = []
        for f in hppfiles:
            if not os.path.exists(f):
                continue
            for l in open(f, 'r').readlines():
                l = l.strip()
                if l.startswith('#include'):
                    includefile = l.split(' ')[1]
                    if len(includefile.split('/')) > 1:
                        includemodule = re.sub('[<>"]', '', includefile.split('/')[0])
                        if includemodule != modulename and includemodule in modules:
                            setfiles.append(includemodule)

        filescount = dict(Counter(setfiles))
        for key, value in sorted(filescount.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            print "  %s: %s" % (key, value)
            g.add_edge(modulename, key, value)

    # Remove nodes
    for n in ['potts']:
        g.remove_vertex(n)

    with open('/Users/giulio/Desktop/data.js', 'w') as fid:
        print '\nNodes'
        fid.write('nodes_vec = [\n')
        for m in modules:
            v = g.get_vertex(m)
            if v is not None:
                log('{id: %d, label: \'%s\'},' % (v.id, v.name), fid)
        fid.write(']\n')

        print '\nEdges'
        fid.write('edges_vec = [\n')
        for m in modules:
            v = g.get_vertex(m)
            if v is not None:
                for a in v.adjacent:
                    log('{from: %d, to: %d, arrows: \'to\'},' % (v.id, a.id), fid)
        fid.write(']')

        print '\nGraph'
        for m in modules:
            v = g.get_vertex(m)
            if v is not None:
                print v