import operator
from typing import (Any, Callable, Generic, Iterable, MutableSequence,
                    NamedTuple, Optional, TypeVar)

T = TypeVar('T')
BO = Callable[[T, T], T]
IE = Callable[[], T]


class Monoid(NamedTuple):
    bo: BO
    ie: IE
    is_group: Optional[Callable[[Any], bool]] = None


class SegumentTree(Generic[T]):
    """セグメント木"""
    monoid: Monoid
    length: int
    data: MutableSequence[T]
    lazy: MutableSequence[T]

    def __init__(self, seq: Iterable[T], monoid: Monoid = Monoid(operator.add, int)) -> None:
        self.monoid = monoid
        data = tuple(seq)
        length = 1
        while len(data) > length:
            length *= 2
        self.length = length
        ie = monoid.ie
        self.data = [ie() for _ in range(len(data) * 4)]
        self.lazy = [ie() for _ in range(len(data) * 4)]
        for i, v in enumerate(data):
            s = i
            e = s + 1
            self.update(s, e, v)

    def eval(self, i: int) -> None:
        lazy = self.lazy[i]
        ie = self.monoid.ie()

        if lazy == ie:
            return

        if i < self.length - 1:
            self.lazy[i * 2 + 1] = lazy
            self.lazy[i * 2 + 2] = lazy

        self.data[i] = lazy
        self.lazy[i] = ie

    def update(self, start: int, end: int, value: T) -> None:
        self._update(start, end, value, 0, 0, self.length)

    def _update(self, a: int, b: int, v: T, k: int, l: int, r: int) -> None:
        self.eval(k)
        if a <= l and r <= b:  # 完全に含む。
            self.lazy[k] = v
            self.eval(k)
        elif a < r and l < b:
            self._update(a, b, v, k * 2 + 1, l, (l + r) // 2)
            self._update(a, b, v, k * 2 + 2, (l + r) // 2, r)
            self.data[k] = self.monoid.bo(self.data[k * 2 + 1], self.data[k * 2 + 2])

    def query(self, start: int, end: int) -> T:
        return self._query(start, end, 0, 0, self.length)

    def _query(self, a: int, b: int, k: int, l: int, r: int) -> T:
        self.eval(k)
        if r <= a or b <= l:  # 交差しない。単位元を返す
            return self.monoid.ie()
        if a <= l and r <= b:  # 完全に含む。
            return self.data[k]
        else:
            vl = self._query(a, b, k * 2 + 1, l, (l + r) // 2)
            vr = self._query(a, b, k * 2 + 2, (l + r) // 2, r)
            return self.monoid.bo(vl, vr)


def main() -> None:
    op: BO
    ie: IE

    mo = Monoid(min, lambda: 100000, lambda v: 0 <= v < 10000)
    # mo = Monoid(max, lambda: -1, lambda v: 0 <= v < 100000)
    # mo = Monoid(operator.add, int)
    # mo = Monoid(operator.mul, lambda: 1)

    n, s, e = 100000, 11, 9374
    # n, s, e = 16, 1, 5

    a = SegumentTree(range(n), mo)
    b = a.query(s, e)

    from functools import reduce
    print(b, reduce(mo.bo, range(s, e)))
    print(a.query(0, n), reduce(mo.bo, range(n)))
    a.update(3, 6, 0)
    print(a.query(s, e))
    print(a.query(3, 7))
    print(a.query(6, 7))
    # print(a.data[:32])
    # print(a.lazy[:32])


if __name__ == '__main__':
    main()
