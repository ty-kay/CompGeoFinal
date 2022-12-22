import random
import math
import heapq

class Action:
    x = 0.0
    y = 0.0
    directrix = None
    process = True
    isPoint = False

    def __init__(self, x, y, directrix, isPoint):
        self.x = x
        self.y = y
        self.directrix = directrix
        self.process = True
        self.isPoint = isPoint

    def deltaX(self, p):
        return self.x - p.x

    def deltaY(self, p):
        return self.y - p.y

    def distance(self, p):
        return math.sqrt(math.pow(self.deltaX(p), 2) + math.pow(self.deltaY(p), 2))

class BeachLine:
    p = None
    prior = None
    next = None
    e = None
    left = None
    right = None

    def __init__(self, p, a, b):
        self.p = p
        self.prior = a
        self.next = b
        self.e = None
        self.left = None
        self.right = None

    def remove(self, s):
        a = self.e.directrix
        if a.prior is not None:
            a.prior.next = a.next
            a.prior.right = s
        if a.next is not None:
            a.next.prior = a.prior
            a.next.left = s
        return a

class Line:
    first = None
    second = None

    def __init__(self, p):
        self.first = p
        self.second = None

    def finish(self, p):
        if self.second is None:
            self.second = p

class PriorityQueue:
    def __init__(self):
        self.pq = []

    def push(self, item):
        entry = [item.x, item]
        heapq.heappush(self.pq, entry)

    def pop(self):
        priority, item = heapq.heappop(self.pq)
        return item

    def empty(self):
        return not self.pq

class Voronoi:
    def __init__(self, points):
        self.output = []
        self.BeachLine = None
        self.points = PriorityQueue()

        for pts in points:
            # tiny offset in case two points have the same x coordinate
            rand = 0.000001 * random.random()
            point = Action(rand + pts[0], pts[1], None, True)
            self.points.push(point)

    def process(self):
        # Determine whether we are processing a point or an event
        while not self.points.empty():
            now = self.points.pop()
            if now.isPoint:
                if self.BeachLine is None:
                    self.BeachLine = BeachLine(now, None, None)
                else:
                    self.arc_insert(now)
            else:
                self.process_event(now)
        self.finish_edges()

    def process_event(self, e):
        if e.process:
            # first new edge
            s = Line(e.y)
            self.output.append(s)

            a = e.directrix.remove(s)

            if a.right is not None:
                a.right.finish(e.y)

            if a.left is not None:
                a.left.finish(e.y)

            # recheck circle events on either side of p
            if a.prior is not None:
                self.check_circle_event(a.prior)
            if a.next is not None:
                self.check_circle_event(a.next)

    def arc_insert(self, p):
            curr = self.BeachLine
            while curr is not None:
                flag, z = self.intersect(p, curr)
                if flag:
                    # new parabola intersects arc i
                    flag, _ = self.intersect(p, curr.next)
                    if (curr.next is not None) and (not flag):
                        curr.next.prior = BeachLine(curr.p, curr, curr.next)
                        curr.next = curr.next.prior
                    else:
                        curr.next = BeachLine(curr.p, curr, None)
                    curr.next.right = curr.right

                    # add p between i and i.next
                    curr.next.prior = BeachLine(p, curr, curr.next)
                    curr.next = curr.next.prior

                    curr = curr.next  # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    # z = self.qwer(p, i)
                    seg = Line(z)
                    self.output.append(seg)
                    curr.prior.right = curr.left = seg

                    seg = Line(z)
                    self.output.append(seg)
                    curr.next.left = curr.right = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(curr)
                    self.check_circle_event(curr.prior)
                    self.check_circle_event(curr.next)

                    return

                curr = curr.next

            # if p never intersects an arc, append it to the list
            curr = self.BeachLine
            while curr.next is not None:
                curr = curr.next
            curr.next = BeachLine(p, curr, None)

            # insert new segment between p and i
            x = -10
            y = (curr.next.p.y + curr.p.y) / 2.0
            first = Action(x, y, None, True)

            seg = Line(first)
            curr.right = curr.next.left = seg
            self.output.append(seg)

    def check_circle_event(self, i):
        # look for a new circle event for arc i
        if i.e is not None:
            i.e.process = False
        i.e = None

        if (i.prior is None) or (i.next is None) or self.CCW(i.prior.p, i.p, i.next.p):
            return

        x, o = self.circle(i.prior.p, i.p, i.next.p)

        i.e = Action(x, o, i, False)
        self.points.push(i.e)

    def CCW (self, a, b, c):
        return ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) >= 0

    def findCenterHelp(self, a, b):
        return b.deltaX(a)*(a.x + b.x) + b.deltaY(a)*(a.y + b.y)


    def circle(self, a, b, c):
        # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = b.deltaX(a)*(b.x + a.x) + b.deltaY(a)*(b.y + a.y)
        F = c.deltaX(a)*(c.x + a.x) + c.deltaY(a)*(c.y + a.y)
        G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

        center = Action((D*E - B*F) / G, (b.deltaX(a)*F - C*E) / G, None, None)

        # o.x plus radius equals max x coord
        x = center.x + a.distance(center)
        o = Action(center.x, center.y, None, True)

        return x, o

    def intersect(self, p, i):
        # check whether a new parabola at point p intersect with arc i
        if (i is None) or (i.p.x == p.x):
            return False, None

        a = 0.0
        b = 0.0

        if i.prior is not None:
            a = (self.intersection(i.prior.p, i.p, 1.0*p.x)).y
        if i.next is not None:
            b = (self.intersection(i.p, i.next.p, 1.0*p.x)).y

        if (((i.prior is None) or (a <= p.y)) and ((i.next is None) or (p.y <= b))):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 -
                        p.x**2) / (2*i.p.x - 2*p.x)
            res = Action(px, py, None, True)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        # get the intersection of two parabolas
        p = p0
        if p0.x == p1.x:
            py = (p0.y + p1.y) / 2.0
        elif p1.x == l:
            py = p1.y
        elif p0.x == l:
            py = p0.y
            p = p1
        else:
            # use quadratic formula
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0/z0 - 1.0/z1
            b = -2.0 * (p0.y/z0 - p1.y/z1)
            c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - \
                1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

            py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)

        px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
        res = Action(px, py, None, True)
        return res

    def finish_edges(self):
        curr = self.BeachLine
        while curr is not None:
            if curr.right is not None and curr.next is not None:
                p = self.intersection(curr.p, curr.next.p, -100)
                curr.right.finish(p)
            curr = curr.next
