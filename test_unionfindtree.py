import pytest

import unionfindtree


def test_union_find_tree_rank():
    tree = unionfindtree.UnionFindTreeRank(10)

    assert tree.unite(1, 2)
    assert not tree.unite(1, 2)

    assert not tree.same(3, 5)
    assert not tree.same(5, 8)
    assert not tree.same(3, 8)
    tree.unite(3, 5)
    tree.unite(5, 8)
    assert tree.same(3, 5)
    assert tree.same(5, 8)
    assert tree.same(3, 8)

    g = frozenset(map(frozenset, tree.groups()))
    assert g == frozenset(map(frozenset, ({0}, {1, 2}, {3, 5, 8}, {4}, {6}, {7}, {9})))


def test_union_find_tree_size():
    tree = unionfindtree.UnionFindTreeSize(10)

    assert tree.unite(1, 2)
    assert not tree.unite(1, 2)

    assert not tree.same(3, 5)
    assert not tree.same(5, 8)
    assert not tree.same(3, 8)
    tree.unite(3, 5)
    tree.unite(5, 8)
    assert tree.same(3, 5)
    assert tree.same(5, 8)
    assert tree.same(3, 8)

    g = frozenset(map(frozenset, tree.groups()))
    assert g == frozenset(map(frozenset, ({0}, {1, 2}, {3, 5, 8}, {4}, {6}, {7}, {9})))

    assert tree.size(0) == 1
    assert tree.size(1) == 2
    assert tree.size(2) == 2


def test_weighted_union_find_tree():
    tree = unionfindtree.WeightUnionFindTree(10)
    assert tree.unite(1, 2, 1)
    assert tree.unite(1, 3, 2)
    assert tree.unite(3, 4, 4)

    assert not tree.same(1, 5)
    assert tree.same(1, 2)
    assert tree.same(1, 3)
    assert tree.same(1, 4)
    assert tree.same(2, 1)
    assert tree.same(2, 3)
    assert tree.same(2, 4)
    assert tree.same(3, 1)
    assert tree.same(3, 2)
    assert tree.same(3, 4)
    assert tree.same(4, 1)
    assert tree.same(4, 2)
    assert tree.same(4, 3)

    assert tree.weight(0) == 0
    assert tree.weight(5) == 0
    assert tree.weight(1) == 0
    assert tree.weight(2) == 1
    assert tree.weight(3) == 2
    assert tree.weight(4) == 6

    assert tree.diff(1, 2) == 1
    assert tree.diff(2, 1) == -1
    assert tree.diff(1, 3) == 2
    assert tree.diff(1, 4) == 6
    assert tree.diff(2, 3) == 1
    assert tree.diff(2, 4) == 5
