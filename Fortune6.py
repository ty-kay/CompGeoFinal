import random
import math
import heapq

class Action:
    x = 0.0
    y = 0.0
    a = None
    valid = True
    isPoint = False

    def __init__(self, x, y, a, isPoint):
        self.x = x
        self.y = y
        self.a = a
        self.valid = True
        self.isPoint = isPoint

class BeachLine:
    p = None
    pprev = None
    pnext = None
    e = None
    s0 = None
    s1 = None

    def __init__(self, p, a=None, b=None):
        self.p = p
        self.pprev = a
        self.pnext = b
        self.e = None
        self.s0 = None
        self.s1 = None

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
            point = Action(rand + pts[0], pts[1], 0.0, True)
            self.points.push(point)

    def process(self):
        # Determine whether we are processing a point or an event
        while not self.points.empty():
            now = self.points.pop()
            if now.isPoint:
                self.arc_insert(now)
            else:
                self.process_event(now)
        self.finish_edges()

    def process_event(self, e):
        if e.valid:
            # first new edge
            s = Line(e.y)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.a
            if a.pprev is not None:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext is not None:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s

            # finish the edges before and after a
            if a.s0 is not None:
                a.s0.finish(e.y)
            if a.s1 is not None:
                a.s1.finish(e.y)

            # recheck circle events on either side of p
            if a.pprev is not None:
                self.check_circle_event(a.pprev, e.x)
            if a.pnext is not None:
                self.check_circle_event(a.pnext, e.x)

    def arc_insert(self, p):
        if self.BeachLine is None:
            self.BeachLine = BeachLine(p)
        else:
            # find the current arcs at p.y
            i = self.BeachLine
            while i is not None:
                flag, z = self.intersect(p, i)
                if flag:
                    # new parabola intersects arc i
                    flag, _ = self.intersect(p, i.pnext)
                    if (i.pnext is not None) and (not flag):
                        i.pnext.pprev = BeachLine(i.p, i, i.pnext)
                        i.pnext = i.pnext.pprev
                    else:
                        i.pnext = BeachLine(i.p, i)
                    i.pnext.s1 = i.s1

                    # add p between i and i.pnext
                    i.pnext.pprev = BeachLine(p, i, i.pnext)
                    i.pnext = i.pnext.pprev

                    i = i.pnext  # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    # z = self.qwer(p, i)
                    seg = Line(z)
                    self.output.append(seg)
                    i.pprev.s1 = i.s0 = seg

                    seg = Line(z)
                    self.output.append(seg)
                    i.pnext.s0 = i.s1 = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(i, p.x)
                    self.check_circle_event(i.pprev, p.x)
                    self.check_circle_event(i.pnext, p.x)

                    return

                i = i.pnext

            # if p never intersects an arc, append it to the list
            i = self.BeachLine
            while i.pnext is not None:
                i = i.pnext
            i.pnext = BeachLine(p, i)

            # insert new segment between p and i
            x = -10
            y = (i.pnext.p.y + i.p.y) / 2.0
            first = Action(x, y, 0.0, True)

            seg = Line(first)
            i.s1 = i.pnext.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, x0):
        # look for a new circle event for arc i
        if i.e is not None:
            i.e.valid = False
        i.e = None

        if (i.pprev is None) or (i.pnext is None):
            return

        if self.CCW(i.pprev.p, i.p, i.pnext.p):
            return

        x, o = self.circle(i.pprev.p, i.p, i.pnext.p)

        i.e = Action(x, o, i, False)
        self.points.push(i.e)

    def CCW (self, a, b, c):
        return ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) >= 0

    def circle(self, a, b, c):
        # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A*(a.x + b.x) + B*(a.y + b.y)
        F = C*(a.x + c.x) + D*(a.y + c.y)
        G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

        # point o is the center of the circle
        ox = (D*E - B*F) / G
        oy = (A*F - C*E) / G

        # o.x plus radius equals max x coord
        x = ox + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)
        o = Action(ox, oy, 0.0, True)

        return x, o

    def intersect(self, p, i):
        # check whether a new parabola at point p intersect with arc i
        if (i is None) or (i.p.x == p.x):
            return False, None

        a = 0.0
        b = 0.0

        if i.pprev is not None:
            a = (self.intersection(i.pprev.p, i.p, 1.0*p.x)).y
        if i.pnext is not None:
            b = (self.intersection(i.p, i.pnext.p, 1.0*p.x)).y

        if (((i.pprev is None) or (a <= p.y)) and ((i.pnext is None) or (p.y <= b))):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 -
                        p.x**2) / (2*i.p.x - 2*p.x)
            res = Action(px, py, 0.0, True)
            return True, res
        return False, None

    def qwer(self, p ,i):
        if (2 * i.p.x == 2 * p.x):
            return None
        a = (self.intersection(i.pprev.p, i.p, 1.0*p.x)).y
        b = (self.intersection(i.p, i.pnext.p, 1.0*p.x)).y

        py = p.y
        px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 -
                    p.x**2) / (2*i.p.x - 2*p.x)
        res = Action(px, py, 0.0, True)
        return res

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
        res = Action(px, py, 0.0, True)
        return res

    def finish_edges(self):
        i = self.BeachLine
        while i.pnext is not None:
            if i.s1 is not None:
                p = self.intersection(i.p, i.pnext.p, -100)
                i.s1.finish(p)
            i = i.pnext

    def get_output(self):
        res = []
        for o in self.output:
            p0 = o.first
            p1 = o.second
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res