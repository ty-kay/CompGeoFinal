import math
import sys

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

    def slope(self, p):
        dx = p.getX() - self.getX()
        dy = p.getY() - self.getY()
        if dx == 0 and dy > 0:
            return math.inf
        if dx == 0 and dy < 0:
            return -math.inf
        if dx == 0 and dy == 0:
            return 0
        return dy / dx

# Function for CCW of 3 points that are on a line
def line (a, b, c):
    ab = a.distance(b)
    bc = b.distance(c)
    ac = c.distance(a)
    if ac <= ab and bc <= ab:
        return 0
    elif ac >= bc:
        return 2
    else:
        return -2

# Calculate CCW of 3 points
def CCW (a, b, c):
    slope1 = a.slope(b)
    # Edge case of slope being positive infinity
    if slope1 == math.inf:
        if c.getX() > a.getX():
            return 1
        if c.getX() < a.getX():
            return -1
        else:
            return line(a, b, c)
    # Edge case of slope being negative infinity
    if slope1 == -math.inf:
        if c.getX() > a.getX():
            return -1
        if c.getX() < a.getX():
            return 1
        else:
            return line(a, b, c)
    # Edge case of a == b
    if slope1 == 0 and a.getX() == b.getX():
        return line(a, b, c)
    # Check whether current going left or right
    flip = 1
    if b.getX() > a.getX():
        flip = -1
    # Check whether above or below the current line
    z = a.getY() - slope1 * (a.getX() - c.getX())
    if c.getY() == z:
        return line(a, b, c)
    if c.getY() > z:
        return flip * 1
    elif c.getY() < z:
        return flip * -1

def Intersect(a, b, c, d):
    first = CCW(a,b,c)
    second = CCW(a,b,d)
    third = CCW(c,d,a)
    fourth = CCW(c,d,b)
    # Parallel lines or a point check because closed line segments
    if first == 0 or second == 0 or third == 0 or fourth == 0:
        return 1
    # Intersecting lines
    if first == -second and third == -fourth:
        return 1
    # Don't intersect
    else:
        return 0

def main():
    arr = []
    for l in sys.stdin:
        arr += l.strip().split()
    first_int = int(arr[0])
    second_int = int(arr[1 + first_int * 6])
    for i in range(1, first_int * 6, 6):
        a = Point(float(arr[i]), float(arr[i + 1]))
        b = Point(float(arr[i + 2]), float(arr[i + 3]))
        c = Point(float(arr[i + 4]), float(arr[i + 5]))
        print(CCW(a, b, c))
    print("\n")
    for i in range(2 + first_int * 6, 2 + first_int * 6 + second_int * 8, 8):
        a = Point(float(arr[i]), float(arr[i + 1]))
        b = Point(float(arr[i + 2]), float(arr[i + 3]))
        c = Point(float(arr[i + 4]), float(arr[i + 5]))
        d = Point(float(arr[i + 6]), float(arr[i + 7]))
        print(Intersect(a, b, c, d))

if __name__ == "__main__":
    main()

