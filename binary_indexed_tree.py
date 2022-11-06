from collections import deque
from typing import (Callable, Generic, Iterable, MutableSequence, NamedTuple,
                    TypeVar)


class BinaryIndexedTree:
    def __init__(self, length):
        self.length = length + 1
        self.data = [0] * self.length

    def add(self, index, v):
        # index += 1
        length = self.length
        data = self.data
        while index < length:
            data[index] += v
            index += (index & -index)

    def update(self, index, v):
        # index += 1
        d = v - (self.query(index) - self.query(index - 1))
        self.add(index, d)

    def query(self, index):
        # index += 1
        data = self.data
        v = 0
        while index > 0:
            v += data[index]
            index -= (index & -index)
        return v


X = TypeVar('X')
FX = Callable[[X, X], X]
EX = Callable[[], X]


def _consume(iterator):
    deque(iterator, maxlen=0)


class Monoid(NamedTuple):
    fx: FX
    ex: EX


class BinaryIndexedTreeG(Generic[X]):
    """BIT こと Binaey Indexed Tree"""
    monoid: Monoid
    length: int
    data: MutableSequence[X]

    def __init__(self, length: int, monoid: Monoid) -> None:
        self.length = length + 1
        ex = monoid.ex
        self.data = [ex() for _ in range(length + 1)]
        self.monoid = monoid

    @classmethod
    def from_seq(cls, seq: Iterable[X], monoid: Monoid) -> None:
        try:
            length = len(seq)
        except:
            data = tuple(seq)
            length = len(data)
        else:
            data = seq
        obj = cls(length, monoid)
        update = obj.update
        # _consume(update(i, v) for i, v in enumerate(data))
        _consume(update(i, v) for i, v in enumerate(data, 1))
        return obj

    def update(self, index: int, v: X) -> None:
        # index += 1
        length = self.length
        fx = self.monoid.fx
        data = self.data
        while index < length:
            data[index] = fx(data[index], v)
            index += (index & -index)

    def query(self, index: int) -> X:
        # index += 1
        fx = self.monoid.fx
        data = self.data
        v = self.monoid.ex()
        while index > 0:
            v = fx(v, data[index])
            index -= (index & -index)
        return v


def main() -> None:
    import operator
    # mo = Monoid(min, lambda: 99999)
    # mo = Monoid(max, int)
    mo = Monoid(operator.add, int)
    # mo = Monoid(operator.mul, lambda: 1)

    L = [3, 1, 4, 1, 5, 9, 2]

    a = BinaryIndexedTree(7)
    for i, v in enumerate(L, 1):
        a.update(i, v)
    A = [a.query(i) for i in range(1, len(L) + 1)]
    print(A)

    b = BinaryIndexedTreeG.from_seq(L, mo)
    B = [b.query(i) for i in range(1, b.length)]
    print(A == B)


if __name__ == '__main__':
    main()
