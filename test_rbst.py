import operator
import random

import pytest

import rbst


@pytest.fixture
def mo():
    return rbst.accumulate_monoid


def test_mutablesequence(mo):
    t = rbst.RBST(mo)
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

    for i, v in enumerate(reversed(t)):
        assert i == 10 - 1 - v

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
    t = rbst.RBST(mo)
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


@pytest.mark.parametrize(
    'seed',
    range(30)
)
def test_addtree(seed):
    gen = random.Random(seed)
    t = rbst.RBST(rbst.accumulate_monoid, gen)

    n = 100
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


@pytest.mark.parametrize(
    'seed',
    range(30)
)
def test_mintree(seed):
    tree = rbst.RBST(rbst.rmq_monoid, random.Random(seed))

    n = 100
    tree.extend(range(n))
    assert tree.get_acc(slice(None)) == 0
    assert tree.get_acc(slice(3, 8)) == 3
    assert tree.get_acc(slice(3, 6)) == 3
    tree.update(3, 6, 10)
    assert tree.get_acc(slice(None)) == 0
    assert tree.get_acc(slice(3, 8)) == 6
    assert tree.get_acc(slice(3, 6)) == 10


def test_mintree_inner():
    tree = rbst.RBST(rbst.rmq_monoid, random.Random(0))

    n = 100
    tree.extend(range(n))
    assert tuple(tree[:10]) == tuple(range(10))
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
