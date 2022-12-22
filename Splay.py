import Fortune6

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.e = None
        self.leftSeg = None
        self.rightSeg = None

class SplayTree:
    def __init__(self):
        self.root = None
        self.header = Node(None)  # For splay()

    def insert(self, key):
        if (self.root == None):
            self.root = Node(key)
            return

        self.splay(key.x)
        if self.root.key.x == key.x:
            # If the key is already there in the tree, don't do anything.
            return

        n = Node(key)
        # CHANGE THESE TO INTERSECTION!
        # Follow this https://jacquesheunis.com/post/fortunes-algorithm/
        flag, z = Fortune6.intersect(key, self.root.key)

        # Just use this? No recursion bc splay trees which is nice
        if flag:
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
        self.root = n

    def remove(self, key):
        self.splay(key)
        if key.x != self.root.key.x:
            # raise 'key not found in tree'
            return

        # Now delete the root.
        if self.root.left == None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x


    def splay(self, key):
        l = r = self.header
        t = self.root
        self.header.left = self.header.right = None
        while True:
            if key.x < t.key.x:
                if t.left == None:
                    break
                if key.x < t.left.key.x:
                    y = t.left
                    t.left = y.right
                    y.right = t
                    t = y
                    if t.left == None:
                        break
                r.left = t
                r = t
                t = t.left
            elif key.x > t.key.x:
                if t.right == None:
                    break
                if key.x > t.right.key.x:
                    y = t.right
                    t.right = y.left
                    y.left = t
                    t = y
                    if t.right == None:
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
