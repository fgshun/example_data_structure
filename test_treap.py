import operator
import random

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
    subt2.update(1, 2, 100)
    assert subt2[1] == 103

    del subt2[1]
    assert tuple(subt2) == (1, 5)
    del t[1::2]
    assert tuple(t) == (0, 2, 4, 6, 8)
    del t[1:4]
    assert tuple(t) == (0, 8)


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


def test_acc(mo):
    gen = random.Random(1)
    t = treap.Treap(mo, gen)
    t.extend([1, 2, 3])
    assert t.root.value == 2
    assert t.root.acc == 6
    assert t.root.left.value == 1
    assert t.root.left.acc == 1
    assert t.root.right.value == 3
    assert t.root.right.acc == 3
    t.update(0, 1, 10)
    assert t.root.value == 2
    assert t.root.acc == 16
    assert t.root.left.value == 11
    assert t.root.left.acc == 11
    assert t.root.right.value == 3
    assert t.root.right.acc == 3
    t.update(2, 3, 100)
    assert t.root.value == 2
    assert t.root.acc == 116
    assert t.root.left.value == 11
    assert t.root.left.acc == 11
    assert t.root.right.value == 103
    assert t.root.right.acc == 103
    t.update(1, 2, 1000)
    assert t.root.value == 1002
    assert t.root.acc == 1116
    assert t.root.left.value == 11
    assert t.root.left.acc == 11
    assert t.root.right.value == 103
    assert t.root.right.acc == 103
    t.update(0, 3, 10000)
    assert t.root.lazy != 0
    t._eval(t.root)
    assert t.root.lazy == 0
    assert t.root.value == 11002
    assert t.root.acc == 31116
    assert t.root.left.lazy != 0
    t._eval(t.root.left)
    assert t.root.left.lazy == 0
    assert t.root.left.value == 10011
    assert t.root.left.acc == 10011
    assert t.root.right.lazy != 0
    t._eval(t.root.right)
    assert t.root.right.lazy == 0
    assert t.root.right.value == 10103  # XXX: 10103 -> 103
    assert t.root.right.acc == 10103  # XXX: 10103 -> 103

    gen = random.Random(4)
    t = treap.Treap(mo, gen)
    t.extend([1, 2, 3])
    assert t.root.value == 3
    t._eval(t.root)
    assert t.root.acc == 6
    t._eval(t.root.left)
    assert t.root.left.value == 1
    assert t.root.left.acc == 3
    t._eval(t.root.right)
    assert t.root.left.right.value == 2
    assert t.root.left.right.acc == 2


@pytest.mark.parametrize(
    'seed',
    range(30)
)
def test_addtree(mo, seed):
    gen = random.Random(seed)
    t = treap.Treap(mo, gen)

    n = 10  # 1000
    sum_n = sum(range(n))
    t.extend(range(n))
    assert t.get_acc(slice(None, None)) == sum_n
    assert t.get_acc(slice(1, 5)) == sum(range(1, 5))
    assert tuple(t[:10]) == tuple(range(10))

    # t._debug_node()
    t.update(1, 5, 10)
    # t._debug_node()
    assert t.get_acc(slice(None, None)) == sum_n + 40
    assert t.get_acc(slice(1, 5)) == sum(range(1, 5)) + 40
    assert tuple(t[:10]) == (0, 11, 12, 13, 14, 5, 6, 7, 8, 9)

    t.update(2, 4, 100)
    assert t.get_acc(slice(None, None)) == sum_n + 40 + 200
    assert tuple(t[:10]) == (0, 11, 112, 113, 14, 5, 6, 7, 8, 9)


def test_mintree():
    mo = treap.Monoid(
        fx=min,
        fa=lambda x, m: m,
        fm=lambda m1, m2: m2,
        fp=lambda m, length: m,
        ex=lambda: 1000000000,
        em=lambda: 1000000000,
        )
    tree = treap.Treap(mo)

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
