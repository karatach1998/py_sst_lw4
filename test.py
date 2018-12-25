import unittest

from main import BTree, Node


class TestBTree(unittest.TestCase):
    def test_create(self):
        t = BTree()
        self.assertIsNotNone(t.root)
        self.assertEqual(t.root.leaf, True)
        self.assertEqual(t.root.n, 0)

    def _assert_btree(self, t, s):
        leaf, n, keys, children = s
        self.assertEqual(t.leaf, leaf)
        self.assertEqual(t.n, n)
        self.assertEqual(t.keys, keys)
        for t, s in zip(t.children, children):
            self._assert_btree(t, s)

    def test_insert(self):
        t = BTree()
        for x in [6, 1, 4, 5, 2, 3, 3]:
            t.insert(x)
        expected_structure = (False, 2, [2, 4], [
            (True, 1, [1], []),
            (True, 2, [3, 3], []),
            (True, 2, [5, 6], [])
        ])
        self._assert_btree(t.root, expected_structure)

    def test_search_empty(self):
        t = BTree()
        self.assertEqual(t.search(3), None)

    def test_search(self):
        t = BTree()
        for x in [5, 1, 4, 2, 3, 3]:
            t.insert(x)
        self.assertEqual(t.search(3), (Node(keys=[3, 3], children=[]), 0))



if __name__ == '__main__':
    unittest.main()
