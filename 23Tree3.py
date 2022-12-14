import random

class Node:
    def __init__(self, val, tree):
        self.tree = tree
        self.val = val
        self._left = None
        self._right = None
        self.parent = None
        # True for black, False for red
        self.black = False
        self.e = None
        self.left = None
        self.right = None

    def flipped(self):
        """Check if this node is flipped"""
        if self.tree is None:
            return False
        return self.tree.flipped

    def left(self):
        return self._left if not self.flipped() else self._right

    def right(self):
        return self._right if not self.flipped() else self._left

    def set_left(self, child):
        if not self.flipped():
            self._left = child
        else:
            self._right = child
        if child is not None:
            child.parent = self

    def set_right(self, child):
        if not self.flipped():
            self._right = child
        else:
            self._left = child
        if child is not None:
            child.parent = self

    def __str__(self) -> str:
        return ("%s:%d:%s" % (
        ('b' if self.black else 'r'), self.val, self.parent if self.parent is None else self.parent.val))


class RedBlackTree:
    def __init__(self):
        self.root = None
        self.flipped = False

    def flip(self):
        """flip the tree: left <-> right"""
        self.flipped = not self.flipped

    def black(self, node):
        """check if a node black (null node is black)"""
        return node is None or node.black

    def _get_node(self, val, node):
        # reach leaf node
        if node is None:
            return None
        if node.val == val:
            return node
        if node.val < val:
            return self._get_node(val, node.right())
        else:
            return self._get_node(val, node.left())

    def has_val(self, val):
        return self._get_node(val, self.root)

    def _insert_leaf(self, node, new_node):
        """
        add a new node to where it should be
        simply dfs find the location and insert
        node is None only when root is None, so just set the root
        """
        if node == None:
            # root node is black
            new_node.black = True
            self.root = new_node
        elif new_node.val < node.val:
            if node.left() is None:
                node.set_left(new_node)
            else:
                self._insert_leaf(node.left(), new_node)
        else:
            if node.right() is None:
                node.set_right(new_node)
            else:
                self._insert_leaf(node.right(), new_node)

    def get_black_parent(self, node):
        if node.black:
            return node
        if node.parent is None:
            return None
        if node.parent.black:
            return node.parent
        if node.parent.parent.black:
            return node.parent.parent
        # node, parent, and grandparent must not be all red
        assert (False)

    def _rotate(self, root, new_root, l, r, lr, rl, root_black=None, l_black=None, r_black=None):
        """
        uniform rotate operation, parameters give the current root and the expected structure and color
        black should be None if no change
        """
        parent = root.parent
        if parent is None:
            self.root = new_root
            new_root.parent = None
        elif parent.left() is root:
            parent.set_left(new_root)
        else:
            parent.set_right(new_root)
        # set color and relationship
        if root_black is not None:
            new_root.black = root_black
        new_root.set_left(l)
        new_root.set_right(r)
        if l is not None:
            l.set_right(lr)
            if l_black is not None:
                l.black = l_black
        if r is not None:
            r.set_left(rl)
            if r_black is not None:
                r.black = r_black

    def _insert_adjust_cluster(self, root):
        """
        adjust a 2-3-4 cluster so that there is no red grandson, return the new root node
        there is at most one red grandson
        """
        left = root.left()
        right = root.right()
        lred = left and not left.black
        rred = right and not right.black
        if lred and rred:
            # if it is a 4 cluster, push black down
            for grandson in [left.left(), left.right(), right.left(), right.right()]:
                if grandson and not grandson.black:
                    root.black = False
                    left.black = True
                    right.black = True
                    # need to adjust parents
                    return root
            return root
        elif lred:
            llred = left.left() and not left.left().black
            lrred = left.right() and not left.right().black
            # ll and lr could not be both red
            assert (not (llred and lrred))
            # let's rotate
            if llred:
                self._rotate(root, left, left.left(), root, left.left().right(), left.right(), True, False, False)
                return left
            elif lrred:
                self._rotate(root, left.right(), left, root, left.right().left(), left.right().right(), True, False,
                             False)
                return left.right()
        elif rred:
            rlred = right.left() and not right.left().black
            rrred = right.right() and not right.right().black
            # ll and lr could not be both red
            assert (not (rlred and rrred))
            # let's _rotate
            if rlred:
                self._rotate(root, right.left(), root, right, right.left().left(), right.left().right(), True, False,
                             False)
                return right.left()
            elif rrred:
                self._rotate(root, right, root, right.right(), right.left(), right.right().left(), True, False, False)
                return right
        return root

    def insert(self, val):
        if self.has_val(val):
            return

        # insert the new value to a leaf node
        new_node = Node(val, self)
        self._insert_leaf(self.root, new_node)

        node = new_node
        # while current node is red, adjust this cluster
        while node is not None and not node.black:
            # find the root of this 2-3-4 cluster
            black = self.get_black_parent(node)

            if black is None:
                # we are at the root
                node.black = True
                node = None
            else:
                node = self._insert_adjust_cluster(black)

    def _predecessor_node(self, node):
        assert node.left() is not None
        node = node.left()
        while node.right() is not None:
            node = node.right()
        return node

    def _successor_node(self, node):
        assert node.right() is not None
        node = node.right()
        while node.left() is not None:
            node = node.left()
        return node

    def delete(self, val):
        """delete a value from the tree"""
        # check if val is in the tree
        node = self._get_node(val, self.root)
        if node is None:
            return
        self._delete_node(node)

    def _delete_node(self, node):
        # if it is an internal node to be deleted
        # substitute by predecessor node
        if node.left() is not None:
            predecessor = self._predecessor_node(node)
            node.val = predecessor.val
            return self._delete_node(predecessor)
        # substitute by successor node
        elif node.right() is not None:
            successor = self._successor_node(node)
            node.val = successor.val
            return self._delete_node(successor)
        # delete leaf node, from bottom to top
        else:
            # if there is only one node, just delete the root
            if node.parent is None:
                self.root = None
                self.flipped = False
                return
            # put the node to the left
            if node is node.parent.right():
                self.flip()
            # if current node is not root, delete first
            node.parent.set_left(None)
            # if current node is red, just over
            if not node.black:
                self.flipped = False
                return
            # if current node is black, bottom-up fix
            parent = node.parent
            node = None
            while node is not self.root:
                # keep the node in the left branch
                if node is parent.right():
                    self.flip()
                pr = parent.right()
                prl = pr.left()
                prr = pr.right()
                if parent.black:
                    if pr.black:
                        if self.black(prl) and self.black(prr):
                            pr.black = False
                            # continue to fix up
                            node = parent
                            parent = node.parent
                            continue
                        elif not self.black(prl):
                            # prl could not be None because red node must exists
                            self._rotate(parent, prl, parent, pr, prl.left(), prl.right(), root_black=True)
                            # fixed
                            break
                        elif not self.black(prr):
                            self._rotate(parent, pr, parent, prr, prl, prr.left(), r_black=True)
                            # fixed
                            break
                    else:
                        prrl = prr.left() if prr is not None else None
                        self._rotate(parent, pr, parent, prr, prl, prrl, root_black=True, l_black=False)
                        # not fixed, continue
                        continue
                else:
                    # pr must be black because parent is red
                    if self.black(prl) and self.black(prr):
                        parent.black = True
                        pr.black = False
                        # fixed
                        break
                    elif not self.black(prr):
                        self._rotate(parent, pr, parent, prr, prl, prr.left(), root_black=False, l_black=True,
                                     r_black=True)
                        # fixed
                        break
                    elif not self.black(prl):
                        self._rotate(parent, prl, parent, pr, prl.left(), prl.right(), l_black=True)
                        # fixed
                        break
        # the root node must be black
        if node is self.root:
            node.black = True
        # reset flip
        self.flipped = False

    def _collect_vals(self, root, arr):
        if root is None:
            return
        self._collect_vals(root.left(), arr)
        arr.append(root.val)
        self._collect_vals(root.right(), arr)

    def get_vals(self):
        ans = []
        self._collect_vals(self.root, ans)
        return ans

    def get_black_depths(self, node, depth, depths):
        if node is None:
            depths.append(depth)
            return
        if node.black:
            depth += 1
        self.get_black_depths(node.left(), depth, depths)
        self.get_black_depths(node.right(), depth, depths)

    def _validate_consequent_red(self, node):
        if node is None:
            return True
        if not node.black and node.parent is not None and not node.parent.black:
            return False
        if not self._validate_consequent_red(node.left()):
            return False
        if not self._validate_consequent_red(node.right()):
            return False
        return True

    def validate(self):
        if self.root is not None and not self.root.black:
            print('root is red:', self.root)
            print(self)
            return False
        depths = []
        self.get_black_depths(self.root, 0, depths)
        if not all(depth == depths[0] for depth in depths):
            print('depths in term of black nodes not the same:', depths)
            print(self)
            return False
        if not self._validate_consequent_red(self.root):
            print('find two consequent red nodes!')
            print(self)
            return False
        return True

    def _to_str(self, node):
        if node is None:
            return ''
        return ' ' + str(node) + ' ' + self._to_str(node.left()) + self._to_str(node.right())

    def __str__(self):
        return self._to_str(self.root)


if __name__ == '__main__':
    for _ in range(10):
        arr = [i for i in range(-1000, 1000)]
        random.shuffle(arr)
        delete = arr[:200]
        random.shuffle(arr)
        tree = RedBlackTree()
