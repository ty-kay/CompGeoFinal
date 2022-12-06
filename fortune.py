# Writing a program that computes Fortune's Algorithm

# Create a point class w/ instances x,y and methods

# Create a parabola class w/ directrix, focus

# Computer Fortune Algorithm

# function AddParabola ( point u )

# function RemoveParabola ( Parabola p )

# function CheckCircleEvent(Parabola p)

# Main method ForLoop (SweepLine)

# Graphics package for printing diagram

# Given a text file, store list of points

# https://blog.ivank.net/fortunes-algorithm-and-implementation.html

# https://pvigier.github.io/2018/11/18/fortune-algorithm-details.html

# https://jacquesheunis.com/post/fortunes-algorithm/

# https://www.cs.hmc.edu/~mbrubeck/voronoi.html

# http://www.bitbanging.space/posts/voronoi-diagram-with-fortunes-algorithm

import sys
import math
import matplotlib.pyplot as plt
import heapq
from queue import PriorityQueue


class arc(object):
    def __init__(self, focus, direc):
        self.focus = focus
        self.direc = direc

    def direc(self):
      # y = y_0
        return self.direc

    def focus(self):
      # x, y point
        return self.focus


def picture(a, b):
    qwer = a
    qwer.append(a[0])
    asdf = b
    asdf.append(b[0])
    plt.plot(qwer, asdf, 'o')
    plt.plot(qwer, asdf, '-')
    plt.show()

# Function to sort the list by second item of tuple


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


def isSiteEvent(x):
    return True


class Node:
    def __init__(self, direct):
        self.direct = direct
        self.nextArc = None
        self.prevArc = None
        self.rightEdge = None
        self.leftEdge = None


class doubly_linked_list:
    def __init__(self):
        self.head = None

    def insert_in_emptylist(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node


# def AddParabola(u):
#     # Create a new arc p with the new site as a focus;
#     p = Parabola(u)

#     # Find where this arc should be located in the beach line. This is given by the x coordinate of the site identifying an arc q as described above;
#     # Add p to the beach line as described above splitting the parabola q in ql and qr;
#     # Delete any vertex event related to the arc q;
#     # Add vertex events for ql and qr (described later);
#     # Create a new Voronoi edge.
def find_parabola_intersection(n1, n2):
    # X coordinate of parabola intersection
    first = n1.direct
    second = n2.direct
    # Use directix and current focus line to determine the x-coordinate intersection

# def AddArc():
    # adding an arc and updating pointers

# def DelArc():
    # deleting an arc and updating pointers


def search(point, beachline):
    p = point
    n = beachline.root
    while n.nextArc != None and find_parabola_intersection(n, n.right) < p[0]:
        n = n.nextArc


def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    points = []
    q = PriorityQueue()
    s = set()
    for j in range(len(arr)):
        if j % 2 == 0:
          # TUPLE
          # (sort by y unless they're identical, in which case sort by x)
            p = (float(arr[j]), float(arr[j + 1]))
            points.append(p)
            s.add(p)
    points = Sort_Tuple(points)
    # add a site event in the event queue for each site
    for p in points:
        q.put((p[1], p))
    # while the event queue is not empty
    BeachLine = doubly_linked_list()
    while not q.empty():
        # pop the top event
        e = q.get()[1]
        print(e)
        # if the event is a site event
        if e in s:
            print("in")
            arc = arc(e)
            BeachLine.insert(arc)
            # Delete vertex event related to arc
            # Add vertex events for ql and qr
            # Create a new Voronoi edge.
        else:
            print("out")
            # Delete the shrinking arc e from the beachline
            # Create a new Voronoi vertex where the two edges intersect
            # Add a new Voronoi edge starting from vertex just added
            # Add vertex events for the arc p.left
            # Add vertex events for the arc p.right


            # create a vertex in the diagram
            # remove the shrunk arc from the beachline
            # delete invalidated events
            # check for new circle events
if __name__ == "__main__":
    main()
