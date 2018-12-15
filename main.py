from dataclasses import dataclass, field


T = 2


@dataclass
class Node:
    keys: list = field(default_factory=list)
    children: list = field(default_factory=list)

    @property
    def n(self):
        return len(self.keys)

    @property
    def leaf(self):
        return len(self.children) == 0

    def _insert(self, k):
        try:
            i, _ = next(filter(lambda t: k < t[1], enumerate(self.keys)))
        except StopIteration:
            i = self.n

        if self.leaf:
            self.keys.insert(i, k)
        else:
            if self.children[i].n == 2 * T - 1:
                self._split(i)
                if k > self.keys[i]:
                    i += 1
            self.children[i]._insert(k)

    def _split(self, i):
        y = self.children[i]
        z = Node(keys=y.keys[T:], children=y.children[T:])
        self.keys.insert(i, y.keys[T-1])
        y.keys, y.children = y.keys[:T-1], y.children[:T-1]
        self.children[i:i+1] = [y, z]

    def _search(self, k):
        i, key = 0, None
        try:
            i, key = next(filter(lambda x: x[1] >= k, enumerate(self.keys)))
        finally:
            if key == k:
                return self, i
            return None if self.leaf else self.children[i]._search(k)



@dataclass
class BTree:
    root: Node = field(default_factory=Node)

    def insert(self, k):
        if self.root.n == 2 * T - 1:
            s = self.root
            self.root = Node(children=[s])
            self.root._split(0)
            s._insert(k)
        else:
            self.root._insert(k)

    def search(self, k):
        return self.root._search(k)
