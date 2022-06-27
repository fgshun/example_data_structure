import operator
from typing import (Callable, Generic, Iterable, MutableSequence, NamedTuple,
                    TypeVar)

"""Lazy Segment Tree

参考 - アルゴリズムロジック - セグメント木を徹底解説！0から遅延評価やモノイドまで
https://algo-logic.info/segment-tree/
"""


X = TypeVar('X')
M = TypeVar('M')
FX = Callable[[X, X], X]
FA = Callable[[X, M], X]
FM = Callable[[M, M], M]
FP = Callable[[M, int], M]
EX = Callable[[], X]
EM = Callable[[], M]


class Monoid(NamedTuple):
    fx: FX
    fa: FA
    fm: FM
    fp: FP
    ex: EX
    em: EM


class LazySegumentTree(Generic[X, M]):
    """遅延評価セグメント木"""
    monoid: Monoid
    length: int
    data: MutableSequence[X]
    lazy: MutableSequence[M]

    def __init__(self, seq: Iterable[X], monoid: Monoid) -> None:
        self.monoid = monoid
        data = tuple(seq)
        length = 1
        while len(data) > length:
            length *= 2
        self.length = length
        ex = monoid.ex
        self.data = [ex() for _ in range(len(data) * 4)]
        em = monoid.em
        self.lazy = [em() for _ in range(len(data) * 4)]
        for i, v in enumerate(data):
            self.data[i + length - 1] = v
        fx = monoid.fx
        for i in range(length - 2, -1, -1):
            self.data[i] = fx(self.data[i * 2 + 1], self.data[i * 2 + 2])

    def eval(self, i: int, length: int) -> None:
        lazy = self.lazy[i]
        em = self.monoid.em()

        if lazy == em:
            return

        if i < self.length - 1:
            self.lazy[i * 2 + 1] = self.monoid.fm(self.lazy[i * 2 + 1], lazy)
            self.lazy[i * 2 + 2] = self.monoid.fm(self.lazy[i * 2 + 2], lazy)

        self.data[i] = self.monoid.fa(self.data[i], self.monoid.fp(lazy, length))
        self.lazy[i] = em

    def update(self, start: int, end: int, value: M) -> None:
        self._update(start, end, value, 0, 0, self.length)

    def _update(self, a: int, b: int, v: M, k: int, l: int, r: int) -> None:
        self.eval(k, r - l)
        if a <= l and r <= b:  # 完全に含む。
            self.lazy[k] = self.monoid.fm(self.lazy[k], v)
            self.eval(k, r - l)
        elif a < r and l < b:
            self._update(a, b, v, k * 2 + 1, l, (l + r) // 2)
            self._update(a, b, v, k * 2 + 2, (l + r) // 2, r)
            self.data[k] = self.monoid.fx(self.data[k * 2 + 1], self.data[k * 2 + 2])

    def query(self, start: int, end: int) -> X:
        return self._query(start, end, 0, 0, self.length)

    def _query(self, a: int, b: int, k: int, l: int, r: int) -> X:
        self.eval(k, r - l)
        if r <= a or b <= l:  # 交差しない。単位元を返す
            return self.monoid.ex()
        if a <= l and r <= b:  # 完全に含む。
            return self.data[k]

        vl = self._query(a, b, k * 2 + 1, l, (l + r) // 2)
        vr = self._query(a, b, k * 2 + 2, (l + r) // 2, r)
        return self.monoid.fx(vl, vr)


def main() -> None:
    # 区間更新 - 区間の最大値
    # mo = Monoid(fx=max,
    #             fa=lambda x, m: m,
    #             fm=lambda m1, m2: m2,
    #             fp=lambda m, length: m,
    #             ex=lambda: -1,
    #             em=lambda: -1,
    #             )
    # 区間更新 - 区間の最小値
    # mo = Monoid(fx=min,
    #             fa=lambda x, m: m,
    #             fm=lambda m1, m2: m2,
    #             fp=lambda m, length: m,
    #             ex=lambda: 1000000000,
    #             em=lambda: 1000000000,
    #             )
    # 区間加算 - 区間の最大値
    # mo = Monoid(fx=max,
    #             fa=operator.add,
    #             fm=operator.add,
    #             fp=lambda m, length: m,
    #             ex=int,
    #             em=int,
    #             )
    # 区間加算 - 区間の合計値
    mo = Monoid(fx=operator.add,
                fa=operator.add,
                fm=operator.add,
                fp=operator.mul,  # lambda m, length: m * length,
                ex=int,
                em=int,
                )

    # n, s, e = 100000000, 11, 9374
    n, s, e = 1000000, 11, 9374
    n, s, e = 16, 1, 5

    a: LazySegumentTree[int, int] = LazySegumentTree(range(n), mo)
    b = a.query(s, e)

    from functools import reduce
    print(b, reduce(mo.fx, range(s, e)))
    print(a.query(0, n), reduce(mo.fx, range(n)))

    print(a.query(3, 7))
    print(a.query(5, 7))
    print(a.query(6, 7))
    a.update(3, 6, 2)
    print(a.query(0, n))
    print(a.query(s, e))
    print(a.query(3, 7))
    print(a.query(5, 7))
    print(a.query(6, 7))
    # print(a.data[:32])
    # print(a.lazy[:32])


if __name__ == '__main__':
    main()
