from __future__ import annotations

import sys
from random import Random
from typing import (ClassVar, Generic, Iterable, Iterator, List,
                    MutableSequence, Optional, Tuple, TypeVar)


class TreapError(Exception):
    pass


T = TypeVar('T')


class Node(Generic[T]):
    random: ClassVar[Random] = Random()

    value: T
    _left: Optional[Node]
    _right: Optional[Node]
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
    def left(self) -> Optional[Node]:
        return self._left

    @left.setter
    def left(self, value: Optional[Node]) -> None:
        self._left = value
        self._update()

    @property
    def right(self) -> Optional[Node]:
        return self._right

    @right.setter
    def right(self, value: Optional[Node]) -> None:
        self._right = value
        self._update()

    def _update(self) -> None:
        self.length = 1
        if self.left is not None:
            self.length += self.left.length
        if self.right is not None:
            self.length += self.right.length

    @classmethod
    def merge(cls, left: Optional[Node], right: Optional[Node]) -> Optional[Node]:
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
    def split(cls, node: Optional[Node], index: int) -> Tuple[Optional[Node], Optional[Node]]:
        if node is None:
            return None, None

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
    def insert(cls, node: Optional[Node], index: int, value: T, priority: Optional[float] = None) -> Node:
        left, right = cls.split(node, index)
        temp = cls.merge(left, Node(value, priority))
        new_node = cls.merge(temp, right)
        if new_node is None:
            raise TreapError()
        return new_node

    @classmethod
    def erase(cls, node: Optional[Node], index: int) -> Optional[Node]:
        left, right = cls.split(node, index + 1)
        temp = cls.split(left, index)[0]
        new_node = cls.merge(temp, right)
        return new_node

    @classmethod
    def find(cls, node: Optional[Node], index: int) -> Optional[Node]:
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


class Treap(MutableSequence[T], Iterable[T]):
    root: Optional[T]

    def __init__(self) -> None:
        self.root = None

    def __getitem__(self, index: int) -> T:
        if not (0 <= index < len(self)):
            raise IndexError()
        node = Node.find(self.root, index)
        return node.value

    def __setitem__(self, index: int, value: T) -> None:
        # TODO: 値の伝搬
        node = self[index]
        node.value = value

    def __delitem__(self, index: int) -> None:
        if not (0 <= index < len(self)):
            raise IndexError()
        self.root = Node.erase(self.root, index)

    def __len__(self) -> int:
        if self.root is None:
            return 0
        return self.root.length

    def insert(self, index: int, value: T) -> None:
        self.root = Node.insert(self.root, index, value)

    def __iter__(self) -> Iterator[T]:
        for index in range(len(self)):
            yield self[index]


def main() -> None:
    pass


if __name__ == '__main__':
    main()
