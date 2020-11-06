from __future__ import annotations

import operator
import sys
from functools import reduce
from random import Random
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator, NamedTuple,
                    MutableSequence, Optional, Tuple, Type, TypeVar, overload)


class TreapError(Exception):
    pass


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


class Node(Generic[X, M]):
    value: X
    acc: X
    lazy: M
    left: Optional[Node[X, M]]
    right: Optional[Node[X, M]]
    length: int
    priority: float

    def __init__(self, value: X, lazy: M, priority: float) -> None:
        self.value = value
        self.acc = value
        self.lazy = lazy
        self.left = None
        self.right = None
        self.length = 1
        self.priority = priority


class Treap(MutableSequence[X], Iterable[X], Generic[X, M]):
    random: ClassVar[Random] = Random()
    root: Optional[Node[X, M]]

    def __init__(self, monoid: Monoid) -> None:
        self.root = None
        self.monoid = monoid

    def _pushup(self, node: Node[X, M]) -> None:
        node.length = 1
        node.acc = node.value
        if node.left is not None:
            node.length += node.left.length
            node.acc = self.monoid.fx(node.acc, node.left.acc)
        if node.right is not None:
            node.length += node.right.length
            node.acc = self.monoid.fx(node.acc, node.right.acc)

    def _eval(self, node: Optional[Node[X, M]]) -> None:
        if node is None:
            return

        em = self.monoid.em()

        if node.lazy == em:
            return

        if node.left:
            node.left.lazy = self.monoid.fm(node.left.lazy, node.lazy)
        if node.right:
            node.right.lazy = self.monoid.fm(node.right.lazy, node.lazy)

        node.value = self.monoid.fa(node.value, node.lazy)
        node.acc = self.monoid.fa(node.acc, self.monoid.fp(node.lazy, node.length))
        node.lazy = em

    def _find(self, index: int) -> Node[X, M]:
        if not (0 <= index < len(self)):
            raise IndexError()
        node = self.root
        while node:
            cnt = node.left.length if node.left else 0
            if cnt > index:
                node = node.left
            elif cnt == index:
                self._eval(node)
                return node
            else:
                node = node.right
                index -= cnt + 1
        raise IndexError()

    def update(self, start: int, end: int, value: M) -> None:
        if self.root is None:
            return
        left, temp = self._split(self.root, start)
        center, right = self._split(temp, end - start)

        assert center
        center.lazy = self.monoid.fm(center.lazy, value)

        temp = self._merge(center, right)
        self.root = self._merge(left, temp)

    @overload
    def __getitem__(self, index: int) -> X:
        ...

    @overload
    def __getitem__(self, index: slice) -> Treap[X, M]:
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            node = self._find(index)
            self._eval(node)
            self._pushup(node)
            return node.value
        elif isinstance(index, slice):
            tree = type(self)(self.monoid)
            start, stop, step = index.indices(len(self))
            for i in range(start, stop, step):
                node = self._find(i)
                self._eval(node)
                self._pushup(node)
                tree.append(node.value)
            return tree
        raise IndexError()

    @overload
    def __setitem__(self, index: int, value: X) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[X]) -> None:
        ...

    def __setitem__(self, index, value):
        # TODO: 置換できるとはかぎらない、これ、 MutableSequence じゃないのでは？
        if isinstance(index, int):
            node = self._find(index)
            node.value = value
            return
        elif isinstance(index, slice):
            values = tuple(value)
            index2 = range(*index.indices(len(self)))
            if len(index2) != len(values):
                raise ValueError('attempt to assign sequence of size {} to extended slice of size {}'.format(
                                 len(values), len(index2)))
            for i, v in zip(index2, values):
                node = self._find(i)
                node.value = v
            return

        raise IndexError()

    def _erase(self, node: Optional[Node[X, M]], index: int) -> Optional[Node[X, M]]:
        left, right = self._split(node, index + 1)
        temp = self._split(left, index)[0]
        new_node = self._merge(temp, right)
        return new_node

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    def __delitem__(self, index):
        if isinstance(index, int):
            if not (0 <= index < len(self)):
                raise IndexError()
            self.root = self._erase(self.root, index)
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            for i in reversed(range(start, stop, step)):
                self.root = self._erase(self.root, i)
        else:
            raise IndexError()

    def __len__(self) -> int:
        if self.root is None:
            return 0
        return self.root.length

    def insert(self, index: int, value: X) -> None:
        left, right = self._split(self.root, index)
        temp = self._merge(left, Node(value, self.monoid.ex(), self.random.random()))
        new_node = self._merge(temp, right)
        if new_node is None:
            raise TreapError()
        self.root = new_node

    def __iter__(self) -> Iterator[X]:
        for index in range(len(self)):
            yield self[index]

    def _split(self, node: Optional[Node[X, M]], index: int) -> Tuple[Optional[Node[X, M]], Optional[Node[X, M]]]:
        if node is None:
            return None, None

        self._eval(node)

        left: Optional[Node[X, M]]
        center: Optional[Node[X, M]]
        right: Optional[Node[X, M]]

        length = node.left.length if node.left is not None else 0
        if length < index:
            center, right = self._split(node.right, index - length - 1)
            left = node
            left.right = center
            self._pushup(left)
        else:
            left, center = self._split(node.left, index)
            right = node
            right.left = center
            self._pushup(right)

        return left, right

    def split(self, index: int) -> Tuple[Treap[X, M], Treap[X, M]]:
        left = type(self)(self.monoid)
        right = type(self)(self.monoid)
        left.root, right.root = self._split(self.root, index)
        return left, right

    def _merge(self, left: Optional[Node[X, M]], right: Optional[Node[X, M]]) -> Optional[Node[X, M]]:
        if left is None:
            return right
        if right is None:
            return left

        self._eval(left)
        self._eval(right)

        if left.priority <= right.priority:
            node = right
            node.left = self._merge(left, node.left)
        else:
            node = left
            node.right = self._merge(node.right, right)
        self._pushup(node)
        return node

    def merge(self, other: Treap[X, M]) -> Treap[X, M]:
        tree = type(self)(self.monoid)
        tree.root = self._merge(self.root, other.root)
        return tree


def main() -> None:
    pass


if __name__ == '__main__':
    main()
