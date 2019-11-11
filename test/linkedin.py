class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        self.idx = Person.count
        Person.count += 1
        self.friends = set()
        self.visited = False

    def __repr__(self):
        return self.name + " [" + ','.join(f for f in list(self.friends)) + "]"


people = []


def addPerson(p):
    if not any(pp.name == p for pp in people):
        people.append(Person(p))


def addFriend(p, f):
    for pp in people:
        if pp.name == p:
            pp.friends.add(f)
            break


def parseConnection(link):
    # Add people
    addPerson(link[0])
    addPerson(link[1])

    # Add friend
    addFriend(link[0], link[1])
    addFriend(link[1], link[0])


def dist(n1, n2, d=0):
    p1 = None
    for p in people:
        if p.name == n1:
            p1 = p
            break
    if p1.visited:
        return len(people) + 1
    p1.visited = True

    if n2 in p1.friends:
        return d + 1
    else:
        distances = []
        for f in p1.friends:
            distances.append(dist(f, n2, d + 1))
        return min(distances)


def numHops(n1, n2):
    for p in people:
        p.visited = False
    d = dist(n1, n2)
    if d < len(people):
        print "distance between " + n1 + " and " + n2 + " is " + str(d)
    else:
        print "No connection between " + n1 + " and " + n2


if __name__ == "__main__":
    connections = [("a", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("b", "f"), ("b", "g"), ("f", "h")]
    for c in connections:
        parseConnection(c)
    print people

    numHops("a", "b")
    numHops("a", "h")
    numHops("a", "i")