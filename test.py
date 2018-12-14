import unittest

from main import BTree


class TestBTree(unittest.TestCase):
    def test_create(self):
        t = BTree()
        self.assertIsNotNone(t.root)
        self.assertEqual(t.root.leaf, True)
        self.assertEqual(t.root.n, 0)


if __name__ == '__main__':
    unittest.main()
