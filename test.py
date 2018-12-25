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
        self.assertEqual(t.keys, keys, 'Keys differ')
        self.assertEqual(len(t.children), len(children),
                        "Children lists have different lengths")
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

    def test_delete_last_in_root_leaf(self):
        t = BTree()
        t.insert(5)
        t.delete(5)
        expected_structure = (True, 0, [], [])
        self._assert_btree(t.root, expected_structure)

    def test_delete_from_empty_tree(self):
        t = BTree()
        t.delete(1)
        expected_structure = (True, 0, [], [])
        self._assert_btree(t.root, expected_structure)

    def test_delete_last_in_leaf_to_force_tree_shrink_in_height(self):
        t = BTree()
        for x in [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
            t.insert(x)
        t.delete(2)
        t.delete(1)
        expected_structure = (False, 1, [7], [
            (False, 1, [5], [
                (True, 2, [3, 4], []),
                (True, 1, [6], []),
            ]),
            (False, 1, [9], [
                (True, 1, [8], []),
                (True, 1, [10], [])
            ])
        ])
        self._assert_btree(t.root, expected_structure)

    def test_delete_not_existing(self):
        t = BTree()
        for x in [1, 2, 3, 4]:
            t.insert(x)
        t.delete(5)
        expected_structure = (False, 1, [2], [
            (True, 1, [1], []),
            (True, 2, [3, 4], [])
        ])
        self._assert_btree(t.root, expected_structure)

    def test_delete_all(self):
        t = BTree()
        for x in [6, 1, 4, 5, 2, 3, 3]:
            t.insert(x)
        for x in [1, 2, 3, 3, 4, 5, 6]:
            t.delete(x)
        expected_structure = (True, 0, [], [])
        self._assert_btree(t.root, expected_structure)


if __name__ == '__main__':
    unittest.main()
