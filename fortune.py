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


class Point(object):
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)" % (self.X, self.Y)

    def getX(self):
        return float(self.X)

    def getY(self):
        return float(self.Y)

    def distance(self, p):
        dx = p.getX() - self.getX()
        dy = p.getY() - self.getY()
        return math.hypot(dx, dy)

    def midpoint(self, p):
        x = (self.getX() + p.getX()) / 2
        y = (self.getY() + p.getY()) / 2
        return Point(x, y)


class Parabola(object):
    def __init__(self, direc, focus):
        self.direc = direc
        self.focus = focus

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
    linkedList = doubly_linked_list()
    while not q.empty():
        # pop the top event
        e = q.get()[1]
        print(e)
        # if the event is a site event
        if e in s:
            print("in")
            # insert a new arc in the beachline
            # check for new circle events
        else:
            print("out")
            # create a vertex in the diagram
            # remove the shrunk arc from the beachline
            # delete invalidated events
            # check for new circle events


if __name__ == "__main__":
    main()
