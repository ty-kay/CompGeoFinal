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
    def __init__(self, point, prior, next):
        self.point = point
        self.prior = prior
        self.next = next
        self.e = None
        self.left = None
        self.right = None

    def remove(self, s):
        curr = self.e.directrix
        if curr.prior is not None:
            curr.prior.next = curr.next
            curr.prior.right = s
        if curr.next is not None:
            curr.next.prior = curr.prior
            curr.next.left = s
        return curr


class Line:
    def __init__(self, point):
        self.first = point
        self.second = None

    def endpoint(self, point):
        if self.second is None:
            self.second = point


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


def update(first, line):
    return (math.pow(first.y, 2) + math.pow(first.x, 2) - math.pow(line, 2)) / (2 * (first.x - line))


def quadratic(first, second, line):
    a = 2 * (first.x - line)
    b = 2 * (second.x - line)
    c = -2 * (first.y / a - second.y / b)
    d = update(first, line)
    e = d - update(second, line)
    py = (-c - math.sqrt(math.pow(c, 2) - 4 * (1 / a - 1 / b) * e)) / (2 * (1 / a - 1 / b))
    return py


def intersection(first, second, line):
    curr = first
    if second.x == line:
        py = second.y
    elif first.x == line:
        py = first.y
        curr = second
    elif first.x == second.x:
        py = (first.y + second.y) / 2
    else:
        py = quadratic(first, second, line)

    px = (math.pow(curr.x, 2) + math.pow((curr.y - py), 2) - math.pow(line, 2)) / (2 * curr.x - 2 * line)
    return Action(px, py, None, True)


def intersect(point, curr):
    if curr is None or curr.point.x == point.x:
        return None

    ret = False
    if curr.prior is None:
        if curr.next is None:
            ret = True
        elif (intersection(curr.point, curr.next.point, point.x)).y >= point.y:
            ret = True
    elif (intersection(curr.prior.point, curr.point, point.x)).y <= point.y:
        if curr.next is None:
            ret = True
        elif (intersection(curr.point, curr.next.point, point.x)).y >= point.y:
            ret = True

    if ret:
        px = (math.pow(curr.point.x, 2) + math.pow((curr.point.y - point.y), 2) - math.pow(point.x, 2))\
             / (2 * curr.point.x - 2 * point.x)
        res = Action(px, point.y, None, True)
        return res
    return None


def CCW(a, b, c):
    return ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) >= 0


def findCenter(a, b):
    return b.deltaX(a) * (a.x + b.x) + b.deltaY(a) * (a.y + b.y)


def circle(first, second, third):
    a = second.deltaX(first) * (second.x + first.x) + second.deltaY(first) * (second.y + first.y)
    b = third.deltaX(first) * (third.x + first.x) + third.deltaY(first) * (third.y + first.y)
    c = 2 * (second.deltaX(first) * (third.y - second.y) - second.deltaY(first) * (third.x - second.x))

    center = Action((third.deltaY(first) * a - second.deltaY(first) * b) / c,
                    (second.deltaX(first) * b - third.deltaX(first) * a) / c, None, None)

    dist = center.x + first.distance(center)
    action = Action(center.x, center.y, None, True)

    return dist, action


def insert(curr, point):
    curr.next.right = curr.right
    curr.next.prior = BeachLine(point, curr, curr.next)
    curr.next = curr.next.prior
    curr = curr.next
    return curr


class Voronoi:
    def __init__(self, points):
        self.BeachLine = None
        self.points = PriorityQueue()
        self.output = []

        for pts in points:
            # tiny offset in case two points have the same x coordinate
            rand = 0.000001 * random.random()
            point = Action(rand + pts[0], pts[1], None, True)
            self.points.push(point)

    def compute(self):
        while not self.points.empty():
            now = self.points.pop()
            if now.isPoint:
                if self.BeachLine is None:
                    self.BeachLine = BeachLine(now, None, None)
                else:
                    self.arc(now)
            else:
                self.event(now)
        self.complete()

    def event(self, event):
        if not event.process:
            return

        s = Line(event.y)
        self.output.append(s)

        a = event.directrix.remove(s)

        if a.right is not None:
            a.right.endpoint(event.y)
        if a.left is not None:
            a.left.endpoint(event.y)
        if a.prior is not None:
            self.circleCheck(a.prior)
        if a.next is not None:
            self.circleCheck(a.next)

    def ray(self, ans):
        ray = Line(ans)
        self.output.append(ray)
        return ray

    def notfound(self, point):
        curr = self.BeachLine
        while curr.next is not None:
            curr = curr.next
        curr.next = BeachLine(point, curr, None)

    def arc(self, point):
        curr = self.BeachLine
        # searching a binary tree
        while curr is not None:
            if curr.point.x != point.x:
                ans = intersect(point, curr)
                if ans is not None:
                    ans2 = intersect(point, curr.next)
                    if (curr.next is None) or (ans2 is not None):
                        curr.next = BeachLine(curr.point, curr, None)
                        curr = insert(curr, point)
                    else:
                        curr.next.prior = BeachLine(curr.point, curr, curr.next)
                        curr.next = curr.next.prior
                        curr = insert(curr, point)

                    ray = self.ray(ans)
                    curr.prior.right = ray
                    curr.left = ray
                    ray2 = self.ray(ans)
                    curr.next.left = ray2
                    curr.right = ray2

                    if curr is not None:
                        self.circleCheck(curr)
                    if curr.prior is not None:
                        self.circleCheck(curr.prior)
                    if curr.next is not None:
                        self.circleCheck(curr.next)

                    return

            curr = curr.next

        self.notfound(point)

        x = -10
        y = (curr.next.point.y + curr.point.y) / 2
        ans = Action(x, y, None, True)

        ray = self.ray(ans)
        curr.right = ray
        curr.next.left = ray

    def circleCheck(self, curr):
        if curr.e is not None:
            curr.e.process = False
        curr.e = None

        if (curr.prior is None) or (curr.next is None) or CCW(curr.prior.point, curr.point, curr.next.point):
            return

        x, o = circle(curr.prior.point, curr.point, curr.next.point)

        curr.e = Action(x, o, curr, False)
        self.points.push(curr.e)

    def complete(self):
        curr = self.BeachLine
        while curr is not None:
            if curr.right is not None and curr.next is not None:
                curr.right.endpoint(intersection(curr.point, curr.next.point, -100))
            curr = curr.next
