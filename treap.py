from __future__ import annotations

import operator
import sys
from functools import reduce
from random import Random
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    MutableSequence, Optional, Tuple, Type, TypeVar, overload)


class TreapError(Exception):
    pass


T = TypeVar('T')


class Node(Generic[T]):
    random: ClassVar[Random] = Random()

    value: T
    _left: Optional[Node[T]]
    _right: Optional[Node[T]]
    length: int
    priority: float

    def __init__(self, value: T, priority: Optional[float]) -> None:
        self.value = value
        self._left = None
        self._right = None
        self.length = 1
        if priority is None:
            priority = self.random.random()
        self.priority = priority

    @property
    def left(self) -> Optional[Node[T]]:
        return self._left

    @left.setter
    def left(self, value: Optional[Node[T]]) -> None:
        self._left = value
        self._update()

    @property
    def right(self) -> Optional[Node[T]]:
        return self._right

    @right.setter
    def right(self, value: Optional[Node[T]]) -> None:
        self._right = value
        self._update()

    def _update(self) -> None:
        self.length = 1
        if self.left is not None:
            self.length += self.left.length
        if self.right is not None:
            self.length += self.right.length

    @classmethod
    def merge(cls, left: Optional[Node[T]], right: Optional[Node[T]]) -> Optional[Node[T]]:
        if left is None:
            return right
        if right is None:
            return left

        if left.priority <= right.priority:
            node = right
            node.left = cls.merge(left, node.left)
        else:
            node = left
            node.right = cls.merge(node.right, right)
        return node

    @classmethod
    def split(cls, node: Optional[Node[T]], index: int) -> Tuple[Optional[Node[T]], Optional[Node[T]]]:
        if node is None:
            return None, None

        left: Optional[Node[T]]
        center: Optional[Node[T]]
        right: Optional[Node[T]]

        length = node.left.length if node.left is not None else 0
        if length >= index:
            left, center = cls.split(node.left, index)
            right = node
            right.left = center
        else:
            center, right = cls.split(node.right, index - length - 1)
            left = node
            left.right = center

        return left, right

    @classmethod
    def insert(cls, node: Optional[Node[T]], index: int, value: T, priority: Optional[float] = None) -> Node[T]:
        left, right = cls.split(node, index)
        temp = cls.merge(left, cls(value, priority))
        new_node = cls.merge(temp, right)
        if new_node is None:
            raise TreapError()
        return new_node

    @classmethod
    def erase(cls, node: Optional[Node[T]], index: int) -> Optional[Node[T]]:
        left, right = cls.split(node, index + 1)
        temp = cls.split(left, index)[0]
        new_node = cls.merge(temp, right)
        return new_node

    @classmethod
    def find(cls, node: Optional[Node[T]], index: int) -> Optional[Node[T]]:
        while node:
            cnt = node.left.length if node.left else 0
            if cnt > index:
                node = node.left
            elif cnt == index:
                return node
            else:
                node = node.right
                index -= cnt + 1
        return None


class LNode(Node[T]):
    acc: T
    _left: Optional[LNode[T]]
    _right: Optional[LNode[T]]
    ie: ClassVar[Any]
    ope: ClassVar[Callable[[Any, Any], T]]

    def __init__(self, value: T, priority: Optional[float]) -> None:
        super().__init__(value, priority)
        self.acc = self.value
        self.lazy = self.ie

    @property
    def left(self) -> Optional[LNode[T]]:
        return self._left

    @left.setter
    def left(self, value: Optional[LNode[T]]) -> None:
        self._left = value
        self._update()

    @property
    def right(self) -> Optional[LNode[T]]:
        return self._right

    @right.setter
    def right(self, value: Optional[LNode[T]]) -> None:
        self._right = value
        self._update()

    def _update(self) -> None:
        super()._update()
        self.acc = reduce(type(self).ope, (
            self.value,
            self.left.acc if self.left else self.ie,
            self.right.acc if self.right else self.ie,
            ))


class AddNode(LNode[int]):
    ie = 0
    ope = operator.add


class MinNode(LNode[Optional[int]]):
    ie = None

    @staticmethod
    def ope(a: Optional[int], b: Optional[int]) -> Optional[int]:
        if a is None:
            return b
        elif b is None:
            return a
        return min(a, b)


class Treap(MutableSequence[T], Iterable[T]):
    node_cls: Type[Node[T]] = Node
    root: Optional[Node[T]]

    def __init__(self) -> None:
        self.root = None

    def _find(self, index: int) -> Node[T]:
        if not (0 <= index < len(self)):
            raise IndexError()
        node = self.node_cls.find(self.root, index)
        if node is None:
            raise IndexError()
        return node

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[T]:
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            node = self._find(index)
            return node.value
        elif isinstance(index, slice):
            tree = self.__class__()
            root = self.root
            start, stop, step = index.indices(len(self))
            for i in range(start, stop, step):
                tree.append(self.node_cls.find(root, i).value)
            return tree
        raise IndexError()

    @overload
    def __setitem__(self, index: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None:
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
            self.root = self.node_cls.erase(self.root, index)
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            for i in reversed(range(start, stop, step)):
                self.root = self.node_cls.erase(self.root, i)
        else:
            raise IndexError()

    def __len__(self) -> int:
        if self.root is None:
            return 0
        return self.root.length

    def insert(self, index: int, value: T) -> None:
        self.root = self.node_cls.insert(self.root, index, value)

    def __iter__(self) -> Iterator[T]:
        for index in range(len(self)):
            yield self[index]

    def split(self, index: int) -> Tuple[Treap, Treap]:
        left = type(self)()
        right = type(self)()
        left.root, right.root = self.node_cls.split(self.root, index)
        return left, right

    def merge(self, other: Treap) -> Treap:
        tree = type(self)()
        tree.root = self.node_cls.merge(self.root, other.root)
        return tree


class AddTreap(Treap[int]):
    node_cls = AddNode


class MinTreap(Treap[Optional[int]]):
    node_cls = MinNode


def main() -> None:
    pass


if __name__ == '__main__':
    main()
