from datetime import datetime
import mysql.connector

#########################
# Parameters
#########################

OUT_FILE = "/Users/giulio/git/_todo_familytree/data.js"

#########################
# Functions
#########################


def getPeople(cursor):
    ret = []
    query = """
    select id, first, last
    from person
    ORDER by id
    """
    cursor.execute(query)
    for x in cursor:
        ret.append(list(x))
    return ret


def getChildren(cursor):
    ret = []
    query = """
    select coupleid, personid
    from child
    ORDER by id
    """
    cursor.execute(query)
    for x in cursor:
        x = list(x)
        x[0] += 1000
        ret.append(x)
    return ret


def getCouple(cursor):
    ret = []
    query = """
    select id, husband, wife
    from couple
    ORDER by id
    """
    cursor.execute(query)
    for x in cursor:
        x = list(x)
        x[0] += 1000
        ret.append(x)
    return ret


def getDepth(l, couple, children):
    parents = []
    for c in couple:
        if c[0] == l:
            parents.append(c[1])
            parents.append(c[2])
    for c in children:
        if c[1] == l:
            parents.append(c[0])
    if len(parents) == 0:
        return 0

    parentsLevel = []
    for p in parents:
        parentsLevel.append(1 + getDepth(p, couple, children))
    return max(parentsLevel)


def getLevel(people, couple, children):
    level = dict()
    for p in people:
        level[p[0]] = -1
    for c in couple:
        level[c[0]] = -1

    # Get all edges
    edges = []
    for c in couple:
        edges.append((c[1], c[0]))
        edges.append((c[2], c[0]))
    for c in children:
        edges.append((c[0], c[1]))

    # Find root nodes (nodes with no input edges)
    nodes = []
    for l in level:
        found = False
        for e in edges:
            if e[1] == l:
                found = True
                break
        if found:
            continue
        nodes.append(l)
        level[l] = 0
    print 'Roots: ', nodes

    # Assign level to all children of roots recursively
    maxdepth = 0
    for n in nodes:
        for e in edges:
            if e[0] == n:
                level[e[1]] = level[e[0]] + 1
                maxdepth = max(maxdepth, level[e[1]])
                nodes.append(e[1])
    print 'Max depth: ', maxdepth

    # Fix level of parents
    fixed = dict()
    for l in level:
        fixed[l] = False
    for d in range(maxdepth, 0, -1):
        # Get all leaves for this level
        nodes = []
        for l in level:
            if level[l] == d:
                found = False
                for e in edges:
                    if e[0] == l:
                        found = True
                        break
                if found:
                    continue
                if fixed[l]:
                    continue
                nodes.append(l)
        print 'Nodes to fix at level %d: %d' % (d, len(nodes))
        for n in nodes:
            fixed[n] = True
            for e in edges:
                if e[1] == n:
                    if not fixed[e[0]]:
                        level[e[0]] = level[e[1]] - 1
                        nodes.append(e[0])
                if e[0] == n:
                    if not fixed[e[1]]:
                        level[e[1]] = level[e[0]] + 1
                        nodes.append(e[1])

    # # Compute level based on ancestors
    # for l in level:
    #     level[l] = getDepth(l, couple, children)
    #
    # # Fix ancestors level for couples and children (must be same level)
    # for i in range(10):
    #     for c in couple:
    #         level[c[1]] = level[c[0]] - 1
    #         level[c[2]] = level[c[0]] - 1
    #     for c in children:
    #         level[c[0]] = max(level[c[0]], level[c[1]] - 1)
    #     for c in children:
    #         level[c[1]] = level[c[0]] + 1

    for c in children:
        if level[c[1]] != level[c[0]] + 1:
            print 'error 1 node ', c[0], c[1], level[c[0]], level[c[1]]
    for c in couple:
        if level[c[1]] != level[c[0]] - 1:
            print 'error 2 node ', c[0], c[1], c[2], level[c[0]], level[c[1]], level[c[2]]
        if level[c[2]] != level[c[0]] - 1:
            print 'error 3 node ', c[0], c[1], c[2], level[c[0]], level[c[1]], level[c[2]]
    for e in edges:
        if level[e[1]] != level[e[0]] + 1:
            print 'error edges ', e[0], e[1]
    for l in level:
        if level[l] < 0:
            print 'error level ', l

    return level


def saveStats(people, couple, children, level, filePath):
    """
    Save stats
    :param batchStats: stats per batch
    :param filePath: output file
    """
    with open(filePath, 'w') as fid:
        fid.write("nodes_vec = [\n")
        for p in people:
            fid.write("{id: %d, label: '%s', group: 0, level: %d},\n" % (p[0], '%d\\n%s %s' % (p[0], p[1], p[2]), level[p[0]]))
            # fid.write("{id: %d, label: '%s %s', group: 0},\n" % (p[0], p[0], ''))
            # fid.write("{id: %d, label: '%s %s', group: 0},\n" % (p[0], p[1], p[2]))
            # fid.write("{id: %d, label: '%s %s', group: 0, level: %d},\n" % (p[0], p[1], p[2], level[p[0]]))
        for c in couple:
            fid.write("{id: %d, label: '%d', group: 1, level: %d},\n" % (c[0], c[0], level[c[0]]))
            # fid.write("{id: %d, label: '%d', group: 1},\n" % (c[0], c[0]))
            # fid.write("{id: %d, label: '', group: 1},\n" % (c[0]))
            # fid.write("{id: %d, label: '', group: 1, level: %d},\n" % (c[0], level[c[0]]))
        fid.write(']\n')

        fid.write("edges_vec = [\n")
        # Get all edges
        edges = []
        for c in couple:
            edges.append((c[1], c[0]))
            edges.append((c[2], c[0]))
        for c in children:
            edges.append((c[0], c[1]))
        edges = sorted(edges, key=lambda e: e[0])
        for e in edges:
            fid.write("{from: %d, to: %d, arrows: 'to'},\n" % (e[0], e[1]))
        fid.write(']\n')

#########################
# Main
#########################


print('Connecting to database')
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="tellme",
    database="familytree")
cursor = mydb.cursor(buffered=True)
print('Connected')

people = getPeople(cursor)
couple = getCouple(cursor)
children = getChildren(cursor)
level = getLevel(people, couple, children)
# print getDepth(43, couple, children)
saveStats(people, couple, children, level, OUT_FILE)
print 'Done'
