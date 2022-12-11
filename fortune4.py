import sys
from queue import PriorityQueue


class Node:
    def __init__(self, direct):
        self.CurrArc = direct
        self.nextArc = None
        self.prevArc = None
        self.rightEdge = None
        self.leftEdge = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None


class arc:
    def __init__(self, direct):
        self.direct = direct

    def getDirec(self):
        return self.direct


def find_parabola_intersection(first, second, line):
    # Find the circle which touches first point, second point, and line
    # Equivalent to finding the intersection of the parabolas first and second
    return

def find_parabola_intersection(first, second, line):
    sol = first
    if first[0] == second[0]:
        sol[1] = (first[1] + second[1]) / 2
    # elif 
    else:
        a = 2 * (first[])

def search(list, arc):
    p = arc.getDirec()
    n = list
    line = p[1]
    while n.nextArc != None and find_parabola_intersection(n, n.right, line) < p[0]:
        n = n.right



def PointEvent(point):
    # Create a new arc p with the new site as a focus;
    arc = arc(point)
    # Find where this arc should be located in the beach line. This is given by the x coordinate of the site identifying an arc q as described above;
    n = search(list, arc)
    # Add p to the beach line as described above splitting the parabola q in ql and qr;
    BeachLine = add(n, arc)
    # Delete any vertex event related to the arc q;
    # Add vertex events for ql and qr (described later);
    # Create a new Voronoi edge.
    return


def VertexEvent(point):
    # Delete the shrinking arc p from the beachline
    # Create a new Voronoi vertex where the two edges intersect
    # Add a new Voronoi edge starting from vertex just added
    # Add vertex events for the arc p.left
    # Add vertex events for the arc p.right
    return


def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    points = []
    q = PriorityQueue()
    for j in range(len(arr)):
        if j % 2 == 0:
            p = (float(arr[j]), float(arr[j + 1]))
            points.append(p)
    # Ty: Sorts by X coordinate in case same Y coordinate
    points = sorted(points, key=lambda x: x[1])
# for each site
# create a site event e,
# e.point = current site, insert e into queue
    for p in points:
        q.put((p[1], (p, True)))
# while queue is not empty
    while not q.empty():
        # e = get the first event from the queue
        e = q.get()[1]
# if its site event
        if e[1] == True:
            print("j")
        else:
            print("k")


if __name__ == "__main__":
    main()
