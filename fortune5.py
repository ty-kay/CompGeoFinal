import sys
from queue import PriorityQueue
from dataStruct import doublyLinkedList
from dataStruct import arc
from dataStruct import segment
from math import sqrt


class Fortune:
    def __init__(self, points):
        self.lines = []
        self.arc = None
        self.events = PriorityQueue

        for p in points:
            self.events.put(p[1], (p, True))

    def process(self):
        while not self.events.empty():
            e = self.events.get()[1]
            if e[1] == True:
                self.proccesPoint(e[0])
            else:
                self.proccessEvent(e[0])
        self.finishEdges()

    def proccesPoint(self, point):
        self.insert(point)

    def proccessEvent(self, point):
        s = segment(point)
        self.lines.append(s)
        # No a right now!
        # Add in a 3rd parameter to the list for beachline?
        a = point.a
        if a.prev is not None:
            a.prev.next = a.next
            a.prev.s1 = a.s
        if a.next is not None:
            a.next.prev = a.prev
            a.next.s0 = s

        if a.s0 is not None:
            a.s0.finish(point)
        if a.s1 is not None:
            a.s1.finish(point)
        if a.prev is not None:
            self.checkCircle(a.prev, point[0])
        if a.next is not None:
            self.checkCircle(a.next, point[0])

    def insert(self, point):
        if self.arc is None:
            self.arc = arc(point)
        else:
            curr = self.arc
            while curr is not None:
                intersect = self.intersect(curr, )

    def intersect(self, point, curr):
        if curr is None:
            return False, None
        if point[0] == curr[0]:
            return False, None
        a, b = 0
        if curr.prev is not None:
            a = self.intersectionPoint()
        else:
            return

    def intersectionPoint(self, point1, point2, l):
        curr = point1
        if point1[0] == point2[0]:
            py = (point2[1] + point1[1]) / 2
        elif point2[0] == l:
            py = point2[1]
        elif point1[0] == l:
            py = point1[1]
            curr = point2
        else:
            x = 2 * (point1[0] - l)
            y = 2 * (point2[0] - l)
            a = 1 / x - 1 / y
            b = -2 * (point1[1] / x - point2[1] / y)
            c = (point1[1]**2 + point1[0]**2 - l**2) / x - \
                (point2[1]**2 + point2[0]**2 - l**2) / y
            py = (-b) - sqrt(b * b - 4 * a * c) / (2 * a)

        px = (curr[0]**2 + (curr[1]-py)**2 - l**2) / (2 * curr[0] - 2 * l)
        pointAns = [px, py]
        return pointAns

    def checkCircle(self, point, x):
        if (point.e is not None) and (point.e[0] != self.x):
            point.e.valid = False
        else:
            point.e.valid = True

        if point.prev is None or point.next is None:
            return

        flag, a, o = self.circle(point.prev.p, point.p, point.next.p)

        if flag and a > self.x:
            self.events.put(point.e)

    def circle(self, a, b, c):
        # check right turn, return false
        # do a bunch of math over here
        return
