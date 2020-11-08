import operator
from typing import (Any, Callable, Generic, Iterable, MutableSequence,
                    NamedTuple, Optional, TypeVar)

X = TypeVar('X')
FX = Callable[[X, X], X]
EX = Callable[[], X]


class Monoid(NamedTuple):
    fx: FX
    ex: EX


class SegumentTree(Generic[X]):
    """セグメント木"""
    monoid: Monoid
    length: int
    data: MutableSequence[X]

    def __init__(self, seq: Iterable[X], monoid: Monoid = Monoid(operator.add, int)) -> None:
        self.monoid = monoid
        data = tuple(seq)
        length = 1
        while len(data) > length:
            length *= 2
        self.length = length
        ex = monoid.ex
        self.data = [ex() for _ in range(len(data) * 4)]
        for i, v in enumerate(data):
            self.data[i + length - 1] = v
        fx = monoid.fx
        for i in range(length - 2, -1, -1):
            self.data[i] = fx(self.data[i * 2 + 1], self.data[i * 2 + 2])

    def update(self, i: int, v: X) -> None:
        index = self.length + i - 1
        self.data[index] = v
        while index > 0:
            index = (index - 1) // 2
            self.data[index] = self.monoid.fx(self.data[index * 2 + 1], self.data[index * 2 + 2])

    def query(self, start: int, end: int) -> X:
        s = start + self.length
        e = end + self.length

        ret = self.monoid.ex()

        while s < e:
            if e & 1:
                e -= 1
                ret = self.monoid.fx(ret, self.data[e - 1])

            if s & 1:
                ret = self.monoid.fx(ret, self.data[s - 1])
                s += 1
            s >>= 1
            e >>= 1

        return ret


def main() -> None:
    # mo = Monoid(min, lambda: 99999)
    # mo = Monoid(max, lambda: 0)
    mo = Monoid(operator.add, int)
    # mo = Monoid(operator.mul, lambda: 1)

    a = SegumentTree(range(100000), mo)
    s, e = 11, 9374
    # s, e = 1, 5
    b = a.query(s, e)

    from functools import reduce
    print(b, reduce(mo.fx, range(s, e)))
    print(a.query(0, 100000), reduce(mo.fx, range(100000)))


if __name__ == '__main__':
    main()
