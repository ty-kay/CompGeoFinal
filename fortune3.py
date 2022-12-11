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
          #  AddParabola( e.point )
            print("j")
        else:
          # RemoveParabola( e.parabola )
            print("k")

            #    function RemoveParabola ( Parabola p )
            #    {
            #       l = an arc lef to p;
            #       r = an arc on the right from p;
            #       if (l or r have their Circle events) remove these events from the queue
            #       s = the circumcenter between l.site, p.site and r.site
            #       x = new edge, starts at s, normal to (l.site, r.site)
            #       finish two neighbour edges xl, xr at point s
            #       replace a sequence xl, p, xr by new edge x
            #       CheckCircleEvent(l);
            #       CheckCircleEvent(r);
            #    }
            #    function CheckCircleEvent(Parabola p)
            #    {
            #       l = arc on the left to p;
            #       r = arc on the right to p;
            #       xl, xr = edges by the p
            #       when there is no l  OR no r  OR  l.site=r.site  RETURN
            #       s = middle point, where xl and xr cross each other
            #       when there is no s (edges go like\ /) RETURN
            #       r = distance between s an p.site (radius of curcumcircle)
            #       if s.y + r is still under the sweepline  RETURN
            #       e = new circle event
            #       e.parabola = p;
            #       e.y = s.y + r;
            #       add e into queue
            #    }


if __name__ == "__main__":
    main()
