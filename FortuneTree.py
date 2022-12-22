import DataType

class Node:
    def __init__(self, data, par=None):
        # print ("Node __init__: " + str(data))
        self.data = list([data])
        self.parent = par
        self.child = list()
        self.arc = None

    def intersect(self, curr, arc):
        # check whether a new parabola at point p intersect with arc i
        if (curr is None):
            return False, None
        if (curr.p.x == arc.x):
            return False, None

        a = 0.0
        b = 0.0

        if i.pprev is not None:
            a = (self.intersection(i.pprev.p, i.p, 1.0 * p.x)).y
        if i.pnext is not None:
            b = (self.intersection(i.p, i.pnext.p, 1.0 * p.x)).y

        if (((i.pprev is None) or (a <= p.y)) and ((i.pnext is None) or (p.y <= b))):
            py = p.y
            px = 1.0 * ((i.p.x) ** 2 + (i.p.y - py) ** 2 -
                        p.x ** 2) / (2 * i.p.x - 2 * p.x)
            res = DataType.ACTION(px, py, 0.0, True)
            return True, res
        return False, None

    def insert(self, arc):
        if self.arc is None:
            self.arc = arc
        else:
            curr = self.arc
            intersect = self.intersect(curr, arc)

