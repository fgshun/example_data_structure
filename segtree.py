import operator
from typing import (Any, Callable, Generic, Iterable, MutableSequence,
                    NamedTuple, Optional, TypeVar)

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


class SegumentTree(Generic[X, M]):
    """セグメント木"""
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
        self.lazy = [ex() for _ in range(len(data) * 4)]
        for i, v in enumerate(data):
            self.data[i + length - 1] = v
        fx = monoid.fx
        for i in range(length - 2, -1, -1):
            self.data[i] = fx(self.data[i * 2 + 1], self.data[i * 2 + 2])

    def eval(self, i: int, length: int) -> None:
        lazy = self.lazy[i]
        ex = self.monoid.ex()

        if lazy == ex:
            return

        if i < self.length - 1:
            self.lazy[i * 2 + 1] = self.monoid.fm(self.lazy[i * 2 + 1], lazy)
            self.lazy[i * 2 + 2] = self.monoid.fm(self.lazy[i * 2 + 2], lazy)

        self.data[i] = self.monoid.fa(self.data[i], self.monoid.fp(lazy, length))
        self.lazy[i] = ex

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
    mo = Monoid(fx=max, 
                fa=lambda x, m: m,
                fm=lambda m1, m2: m2,
                fp=lambda m, length: m,
                ex=lambda: -1,
                em=lambda: -1,
                )
    mo = Monoid(fx=min, 
                fa=lambda x, m: m,
                fm=lambda m1, m2: m2,
                fp=lambda m, length: m,
                ex=lambda: 100000,
                em=lambda: 100000,
                )
    mo = Monoid(fx=operator.add, 
                fa=operator.add,
                fm=operator.add,
                fp=lambda m, length: m * length,
                ex=int,
                em=int,
                )

    n, s, e = 100000, 11, 9374
    # n, s, e = 16, 1, 5

    a: SegumentTree[int, int] = SegumentTree(range(n), mo)
    b = a.query(s, e)

    from functools import reduce
    print(b, reduce(mo.fx, range(s, e)))
    print(a.query(0, n), reduce(mo.fx, range(n)))

    print(a.query(3, 7))
    print(a.query(5, 7))
    print(a.query(6, 7))
    a.update(3, 6, 1)
    print(a.query(0, n))
    print(a.query(s, e))
    print(a.query(3, 7))
    print(a.query(5, 7))
    print(a.query(6, 7))
    # print(a.data[:32])
    # print(a.lazy[:32])


if __name__ == '__main__':
    main()
