import operator

import pytest

import treap


@pytest.fixture
def mo():
    monoid = treap.Monoid(
        fx=operator.add,
        fa=operator.add,
        fm=operator.add,
        fp=lambda m, length: m * length,
        ex=int,
        em=int,
        )
    return monoid


def test_mutablesequence(mo):
    t = treap.Treap(mo)
    assert t.index
    assert len(t) == 0

    for i in range(10):
        t.append(i)

    assert len(t) == 10
    assert t.index(3) == 3
    with pytest.raises(ValueError):
        t.index(11)

    for i, v in enumerate(t):
        assert i == v

    t.insert(3, 100)
    assert len(t) == 11
    assert t[2] == 2
    assert t[3] == 100
    assert t[4] == 3

    del t[3]
    assert len(t) == 10
    assert t[2] == 2
    assert t[3] == 3


def test_slicing(mo):
    t = treap.Treap(mo)
    for i in range(10):
        t.append(i)
    subt = t[1:4]
    assert len(subt) == 3
    assert tuple(subt) == (1, 2, 3)
    assert len(t) == 10
    assert tuple(t) == tuple(range(10))

    subt2 = t[1:6:2]
    assert len(subt2) == 3
    assert tuple(subt2) == (1, 3, 5)
    assert len(t) == 10
    assert tuple(t) == tuple(range(10))

    assert subt2[1] == 3
    subt2[1] = 100
    assert subt2[1] == 100

    with pytest.raises(ValueError):
        t[1::2] = (1, 2, 3, 4)
    with pytest.raises(ValueError):
        t[1::2] = (1, 2, 3, 4, 5, 6)
    t[1::2] = (100, 101, 102, 103, 104)
    assert tuple(t) == (0, 100, 2, 101, 4, 102, 6, 103, 8, 104)

    del subt2[1]
    assert tuple(subt2) == (1, 5)
    del t[1::2]
    assert tuple(t) == (0, 2, 4, 6, 8)


def test_split(mo):
    t = treap.Treap(mo)

    a = treap.Node(10, 0, 0.5)
    b = treap.Node(20, 0, 0.25)
    c = t._merge(a, b)
    d = treap.Node(30, 0, 0.75)
    e = t._merge(c, d)
    f, g = t._split(e, 1)

    assert f.length == 1
    assert f.value == 10
    assert g.length == 2
    assert g.value == 30


def test_merge(mo):
    t = treap.Treap(mo)

    a = treap.Node(10, 0, 0.5)
    b = treap.Node(20, 0, 0.25)
    c = t._merge(a, b)

    assert c
    assert c.length == 2
    assert c.value == 10
    assert c.left is None
    assert c.right
    assert c.right.length == 1
    assert c.right.value == 20

    d = treap.Node(30, 0, 0.75)
    e = t._merge(c, d)

    assert e.length == 3
    assert e.value == 30
    assert e.left
    assert e.left.value == 10
    assert e.right is None


@pytest.mark.skip
def test_addtree():
    tree = treap.AddTreap()

    tree.extend(range(10))
    assert tuple(tree) == tuple(range(10))
    assert tree.root.acc == sum(range(10))


@pytest.mark.skip
def test_mintree():
    tree = treap.MinTreap()

    tree.extend(range(10))
    assert tuple(tree) == tuple(range(10))
    assert tree.root.acc == 0

    left, temp = tree.split(3)
    center, right = temp.split(5)

    assert left.root.acc == 0
    assert center.root.acc == 3
    assert right.root.acc == 3 + 5

    temp = center.merge(right)
    assert temp.root.acc == 3

    tree = left.merge(temp)
    assert tree.root.acc == 0
