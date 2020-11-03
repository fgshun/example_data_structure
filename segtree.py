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
    mo: Monoid
    length: int
    data: MutableSequence[T]

    def __init__(self, seq: Iterable[T], monoid: Monoid = Monoid(operator.add, int)) -> None:
        self.monoid = monoid
        data = tuple(seq)
        length = 1
        while len(data) > length:
            length *= 2
        self.length = length
        ie = monoid.ie
        self.data = [ie() for _ in range(len(data) * 4)]
        for i, v in enumerate(data):
            self.update(i, v)

    def update(self, i: int, v: T) -> None:
        if self.monoid.is_group:
            assert self.monoid.is_group(v)
        index = self.length + i - 1
        self.data[index] = v
        while index > 0:
            index = (index - 1) // 2
            self.data[index] = self.monoid.bo(self.data[index * 2 + 1], self.data[index * 2 + 2])

    def query(self, start: int, end: int) -> T:
        return self._query(start, end, 0, 0, self.length)

    def _query(self, a: int, b: int, k: int, l: int, r: int) -> T:
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

    a = SegumentTree(range(10000), mo)
    s, e = 11, 9374
    # s, e = 1, 5
    b = a.query(s, e)

    from functools import reduce
    print(b, reduce(mo.bo, range(s, e)))
    print(a.query(0, 10000), reduce(mo.bo, range(10000)))


if __name__ == '__main__':
    main()
