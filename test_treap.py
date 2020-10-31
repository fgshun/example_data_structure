import treap

import pytest


def test_merge():
    a = treap.Node(10, 0.5)
    b = treap.Node(20, 0.25)
    c = treap.Node.merge(a, b)

    assert c
    assert c.length == 2
    assert c.value == 10
    assert c.left is None
    assert c.right
    assert c.right.length == 1
    assert c.right.value == 20

    d = treap.Node(30, 0.75)
    e = treap.Node.merge(c, d)

    assert e.length == 3
    assert e.value == 30
    assert e.left
    assert e.left.value == 10
    assert e.right is None


def test_split():
    a = treap.Node(10, 0.5)
    b = treap.Node(20, 0.25)
    c = treap.Node.merge(a, b)
    d = treap.Node(30, 0.75)
    e = treap.Node.merge(c, d)
    f, g = treap.Node.split(e, 1)

    assert f.length == 1
    assert f.value == 10
    assert g.length == 2
    assert g.value == 30


def test_treap():
    t = treap.Treap()
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


def test_slicing():
    t = treap.Treap()
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
