import unittest

from main import BTree


class TestBTree(unittest.TestCase):
    def test_create(self):
        t = BTree()
        self.assertIsNotNone(t.root)
        self.assertEqual(t.root.leaf, True)
        self.assertEqual(t.root.n, 0)

    def _compare_btree(self, t, s):
        leaf, n, keys, children = s
        self.assertEqual(t.leaf, leaf)
        self.assertEqual(t.n, n)
        self.assertEqual(t.keys, keys)
        for t, s in zip(t.children, children):
            self._compare_btree(t, s)

    def test_insert(self):
        t = BTree()
        for x in [5, 1, 4, 2, 3, 3]:
            t.insert(x)
        print(t)
        self.assertEqual(t.root.leaf, False)
        expected_structure = (False, 2, [2, 4], [
            (True, 1, [1], []),
            (True, 2, [3, 3], []),
            (True, 1, [5], [])
        ])
        self._compare_btree(t.root, expected_structure)


if __name__ == '__main__':
    unittest.main()
