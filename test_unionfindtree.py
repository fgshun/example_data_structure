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
