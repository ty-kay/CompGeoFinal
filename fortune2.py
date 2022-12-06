import sys
import math
import matplotlib.pyplot as plt
import heapq
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

    def insert(self, point1, point2):
        point2.prevArc.nextArc = point1
        # Update everything properly when inserting into the linkedList
        # and splitting the previous arc into two arcs


def find_parabola_intersection(first, second):
    # Directix = focusP[1]
    # We have the focus for both lines
    # We can use this to determine where they intersect
    return 1


def PointEvent(e, BeachLine):
    focusP = e
    n = BeachLine.root
    while n.right != None and find_parabola_intersection(n, n.right, focusP) < focusP[0]:
        n = n.right
    curr = n
  # Add p to the beach line as described above splitting the parabola q in ql and qr;
    BeachLine.insert(focusP, curr)


def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    points = []
    q = PriorityQueue()
    s = set()
    for j in range(len(arr)):
        if j % 2 == 0:
            # Generate all points as tuples
            p = (float(arr[j]), float(arr[j + 1]))
            points.append(p)
            s.add(p)
    # Sorts by X coordinate
    points = sorted(points, key=lambda x: x[1])
    # add a site event in the event queue for each site
    for p in points:
        q.put((p[1], p))
    BeachLine = DoublyLinkedList
    # while the event queue is not empty
    while not q.empty():
        # pop the top event
        e = q.get()[1]
        print(e)
        # if the event is a point event
        if e in s:
            PointEvent(e, BeachLine)
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
