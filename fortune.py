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


def AddParabola(u):
    # par = arc under point u;
    par = u
    # if (par has its circle event, when it is removed form the beachline)

    #    remove this event form the queue
    # new arcs a, b, c;
    # b.site = u;
    # a.site = c.site = par.site; // site of arc is a focus of arc
    # xl, xr  = left and right edges, which comes from point on par under u
    # xl is a normal to  (a.site, b.site);
    # xr is a normal to (b.site, c.site);
    # replace par by the sequence a, xl, b, xr, c
    # CheckCircleEvent(a);
    # CheckCircleEvent(c);


def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    points = []
    q = PriorityQueue()
    for j in range(len(arr)):
        if j % 2 == 0:
          # TUPLE
          # (sort by y unless they're identical, in which case sort by x)
            p = (float(arr[j]), float(arr[j + 1]))
            points.append(p)
    points = Sort_Tuple(points)
    for p in points:
        q.put((p[1], p))
    while not q.empty():
        e = q.get()
        if isSiteEvent(e):
            AddParabola(e)


if __name__ == "__main__":
    main()
