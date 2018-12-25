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
        y.keys, y.children = y.keys[:T-1], y.children[:T]
        self.children[i:i+1] = [y, z]

    def _search(self, k):
        i, key = next(filter(lambda x: x[1] >= k, enumerate(self.keys)), (0, None))
        if key == k:
            return self, i
        return None if self.leaf else self.children[i]._search(k)

    def _delete(self, k):
        # NOTE(sergey): Everywhere below x, y, z marks tree nodes
        # in the following relation:
        #
        #    x[=self]
        #      / \
        #     y   z

        i, key = next(filter(lambda x: x[1] >= k, enumerate(self.keys)), (self.n, None))
        if key == k:
            if self.leaf:
                self.keys.pop(i)
                return

            y = self.children[i]
            z = self.children[i + 1]
            if y.n >= T:
                self.keys[i] = y.keys[-1]
                y._delete(y.keys[-1])
            elif z.n >= T:
                self.keys[i] = z.keys[0]
                z._delete(z.keys[0])
            else:
                self._merge(i)
                y._delete(k)
        else:
            if self.leaf:
                return

            y = self.children[i]
            if y.n == T - 1:
                if i == self.n:
                    i -= 1
                    y = self.children[i]
                z = self.children[i + 1]
                if z.n >= T:
                    y.keys.append(self.keys[i])
                    self.keys[i] = z.keys.pop(0)
                    if not z.leaf:
                        y.children.append(z.children.pop(0))
                else:
                    self._merge(i)
            y._delete(k)

    def _merge(self, i):
        y = self.children[i]
        z = self.children[i + 1]
        k = self.keys[i]

        y.keys.append(k)
        y.keys.extend(z.keys)
        y.children.extend(z.children)
        self.keys.pop(i)
        self.children.pop(i + 1)


@dataclass
class BTree:
    root: Node = field(default_factory=Node)

    def insert(self, k):
        if self.root.n == 2 * T - 1:
            r = self.root
            self.root = Node(children=[r])
            self.root._split(0)
            self.root._insert(k)
        else:
            self.root._insert(k)

    def search(self, k):
        return self.root._search(k)

    def delete(self, k):
        self.root._delete(k)
        if self.root.n == 0 and not self.root.leaf:
            self.root = self.root.children.pop()
