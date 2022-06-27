import operator

from lazysegtree import LazySegumentTree, Monoid


def test_lazy_seg_tree0():
    # 区間加算 - 区間の合計値
    mo = Monoid(fx=operator.add,
                fa=operator.add,
                fm=operator.add,
                fp=operator.mul,  # lambda m, length: m * length,
                ex=int,
                em=int,
                )
    a: LazySegumentTree[int, int] = LazySegumentTree((0,) * 10, mo)

    assert a.query(0, 10) == 0
    assert a.query(0, 1) == 0

    a.update(0, 3, 1)  # 1 1 1 0
    a.update(1, 2, 2)  # 0 2 0 0
    a.update(2, 4, 4)  # 0 0 4 4
    # 1 3 5 4

    assert a.query(0, 1) == 1
    assert a.query(0, 2) == 4
    assert a.query(0, 3) == 9
    assert a.query(0, 4) == 13
    assert a.query(1, 2) == 3
    assert a.query(1, 3) == 8
    assert a.query(1, 4) == 12
    assert a.query(2, 3) == 5
    assert a.query(2, 4) == 9
    assert a.query(3, 4) == 4


def test_lazy_seg_tree1():
    # 区間加算 - 区間の最大値
    mo = Monoid(fx=max,
                fa=operator.add,
                fm=operator.add,
                fp=lambda m, length: m,
                ex=int,
                em=int,
                )
    a: LazySegumentTree[int, int] = LazySegumentTree((0,) * 10, mo)

    assert a.query(0, 10) == 0
    assert a.query(0, 1) == 0

    a.update(0, 3, 1)  # 1 1 1 0
    a.update(1, 2, 2)  # 0 2 0 0
    a.update(2, 4, 4)  # 0 0 4 4
    # 1 3 5 4

    assert a.query(0, 1) == 1
    assert a.query(0, 2) == 3
    assert a.query(0, 3) == 5
    assert a.query(0, 4) == 5
    assert a.query(1, 2) == 3
    assert a.query(1, 3) == 5
    assert a.query(1, 4) == 5
    assert a.query(2, 3) == 5
    assert a.query(2, 4) == 5
    assert a.query(3, 4) == 4


def test_lazy_seg_tree2():
    # 区間更新 - 区間の最大値
    mo = Monoid(fx=max,
                fa=lambda x, m: m,
                fm=lambda m1, m2: m2,
                fp=lambda m, length: m,
                ex=lambda: -1,
                em=lambda: -1,
                )
    a: LazySegumentTree[int, int] = LazySegumentTree((0,) * 10, mo)

    assert a.query(0, 10) == 0
    assert a.query(0, 1) == 0

    a.update(0, 3, 1)  # 1 1 1 -
    a.update(1, 2, 2)  # - 2 - -
    a.update(2, 4, 4)  # - - 4 4
    # 1 2 4 4

    assert a.query(0, 1) == 1
    assert a.query(0, 2) == 2
    assert a.query(0, 3) == 4
    assert a.query(0, 4) == 4
    assert a.query(1, 2) == 2
    assert a.query(1, 3) == 4
    assert a.query(1, 4) == 4
    assert a.query(2, 3) == 4
    assert a.query(2, 4) == 4
    assert a.query(3, 4) == 4


def test_lazy_seg_tree3():
    # 区間更新 - 区間の最小値
    mo = Monoid(fx=min,
                fa=lambda x, m: m,
                fm=lambda m1, m2: m2,
                fp=lambda m, length: m,
                ex=lambda: 1000000000,
                em=lambda: 1000000000,
                )
    a: LazySegumentTree[int, int] = LazySegumentTree((0,) * 10, mo)

    assert a.query(0, 10) == 0
    assert a.query(0, 1) == 0

    a.update(0, 3, 1)  # 1 1 1 -
    a.update(1, 2, 2)  # - 2 - -
    a.update(2, 4, 4)  # - - 4 4
    # 1 2 4 4

    assert a.query(0, 1) == 1
    assert a.query(0, 2) == 1
    assert a.query(0, 3) == 1
    assert a.query(0, 4) == 1
    assert a.query(1, 2) == 2
    assert a.query(1, 3) == 2
    assert a.query(1, 4) == 2
    assert a.query(2, 3) == 4
    assert a.query(2, 4) == 4
    assert a.query(3, 4) == 4
