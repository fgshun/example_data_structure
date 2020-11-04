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
    lazy: M
    left: Optional[Node[X, M]]
    right: Optional[Node[X, M]]
    length: int
    priority: float

    def __init__(self, value: X, lazy: M, priority: float) -> None:
        self.value = value
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

    def _find(self, index: int) -> Node[X, M]:
        if not (0 <= index < len(self)):
            raise IndexError()
        node = self.root
        while node:
            cnt = node.left.length if node.left else 0
            if cnt > index:
                node = node.left
            elif cnt == index:
                return node
            else:
                node = node.right
                index -= cnt + 1
        if node is None:
            raise IndexError()
        return node

    @overload
    def __getitem__(self, index: int) -> X:
        ...

    @overload
    def __getitem__(self, index: slice) -> Treap[X, M]:
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            node = self._find(index)
            return node.value
        elif isinstance(index, slice):
            tree = type(self)(self.monoid)
            start, stop, step = index.indices(len(self))
            for i in range(start, stop, step):
                tree.append(self._find(i).value)
            return tree
        raise IndexError()

    @overload
    def __setitem__(self, index: int, value: X) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[X]) -> None:
        ...

    def __setitem__(self, index, value):
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

        left: Optional[Node[X, M]]
        center: Optional[Node[X, M]]
        right: Optional[Node[X, M]]

        length = node.left.length if node.left is not None else 0
        if length < index:
            center, right = self._split(node.right, index - length - 1)
            left = node
            left.right = center
            self._update(left)
        else:
            left, center = self._split(node.left, index)
            right = node
            right.left = center
            self._update(right)

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

        if left.priority <= right.priority:
            node = right
            node.left = self._merge(left, node.left)
        else:
            node = left
            node.right = self._merge(node.right, right)
        self._update(node)
        return node

    def merge(self, other: Treap[X, M]) -> Treap[X, M]:
        tree = type(self)(self.monoid)
        tree.root = self._merge(self.root, other.root)
        return tree

    def _update(self, node: Node[X, M]) -> None:
        node.length = 1
        if node.left is not None:
            node.length += node.left.length
        if node.right is not None:
            node.length += node.right.length


def main() -> None:
    pass


if __name__ == '__main__':
    main()
