class Node:
    def __init__(self, p, left, right):
        self.p = p
        self.left = left
        self.right = right
        self.e = None
        self.left = None
        self.right = None

    def equals(self, node):
        return self.p.x == node.p.x


class SplayTree:
    def __init__(self):
        self.root = None
        self.header = Node(None, None, None)  # For splay()

    def insert(self, point):
        if self.root is None:
            self.root = Node(point, None, None)
            return

        self.splay(point)
        if self.root.p.x == point.x:
            # If the key is already there in the tree, don't do anything.
            return

        n = Node(point.x)
        if point.x < self.root.p.x:
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
        self.root = n


    def remove(self, key, s):
        self.splay(key)
        if key.x != self.root.key.x:
            return
#             a = e.a
#             if a.pprev is not None:
#                 a.pprev.pnext = a.pnext
#                 a.pprev.s1 = s
#             if a.pnext is not None:
#                 a.pnext.pprev = a.pprev
#                 a.pnext.s0 = s
#
#             # finish the edges before and after a
#             if a.s0 is not None:
#                 a.s0.finish(e.p)
#             if a.s1 is not None:
#                 a.s1.finish(e.p)

        # Now delete the root.
        if self.root.left is None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x
        if self.root.left is not None:
            self.root.left.s1 = s
        if self.root.right is not None:
            self.root.right.s0 = s

    def find(self, key):
        if self.root is None:
            return None
        self.splay(key)
        if self.root.x != key.x:
            return None
        # Key or X?
        return self.root.p

    def isEmpty(self):
        return self.root is None

    def splay(self, key):
        l = r = self.header
        t = self.root
        self.header.left = self.header.right = None
        while True:
            if key.x < t.x:
                if t.left is None:
                    break
                if key.x < t.left.x:
                    y = t.left
                    t.left = y.right
                    y.right = t
                    t = y
                    if t.left is None:
                        break
                r.left = t
                r = t
                t = t.left
            elif key.x > t.x:
                if t.right is None:
                    break
                if key.x > t.right.x:
                    y = t.right
                    t.right = y.left
                    y.left = t
                    t = y
                    if t.right is None:
                        break
                l.right = t
                l = t
                t = t.right
            else:
                break
        l.right = t.left
        r.left = t.right
        t.left = self.header.right
        t.right = self.header.left
        self.root = t
