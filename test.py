import unittest

from main import BTree


class TestBTree(unittest.TestCase):
    def test_create(self):
        t = BTree()
        self.assertIsNotNone(t.root)
        self.assertEqual(t.root.leaf, True)
        self.assertEqual(t.root.n, 0)

    def _compare_btree(t, s):
        leaf, n, keys, children = s
        assertEqual(t.leaf, leaf)
        assertEqual(t.n, n)
        assertEqual(t.keys, keys)
        for t, s in zip(t.children, children):
            _compare_btree(t, s)

    def test_insert(self):
        t = BTree()
        for x in [5, 1, 4, 2, 3, 3]:
            t.insert(x)
        self.assertEqual(t.root.leaf, False)
        expected_structure = (False, [], [])


if __name__ == '__main__':
    unittest.main()
