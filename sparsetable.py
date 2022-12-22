from itertools import islice, tee, repeat, starmap
from typing import Callable, Iterable, Iterator, Generic, Sequence, TypeVar


T = TypeVar('T')
Operator = Callable[[T, T], T]


class SparseTable(Generic[T]):
    def __init__(self, values: Iterable[T], op: Operator) -> None:
        self.op: Operator = op
        self.table: Sequence[Sequence[T]] = tuple(self._init_table(values, op))

    @staticmethod
    def _init_table(values: Iterable[T], op: Operator) -> Iterator[Sequence[T]]:
        temp = tuple(values)
        length = len(temp)
        table_size = (length - 1).bit_length()

        yield temp
        k = 1
        for _ in repeat(None, table_size):
            it0, it1 = tee(temp)
            it = zip(it0, islice(it1, k, None))
            temp = tuple(starmap(op, it))
            yield temp
            k <<= 1

    def query(self, left: int, right: int) -> T:
        length = right - left
        if length < 0:
            raise ValueError
        index = length.bit_length() - 1
        table = self.table[index]
        return self.op(table[left], table[right - 2 ** index])

    def __len__(self) -> int:
        return len(self.table[0])


def main() -> None:
    from random import randint
    length = 8
    seq: Sequence[int] = [randint(0, 100) for _ in range(length)]
    print(f'{seq=}')
    sparse_table: SparseTable[int] = SparseTable(seq, max)
    for k, table in enumerate(sparse_table.table):
        print(f'{k=} {table=}')
    
    for _ in range(10):
        L = randint(0, length - 1)
        R = randint(0, length - 1)
        if L > R:
            L, R = R, L
        R += 1

        print(L, R, sparse_table.query(L, R))


if __name__ == '__main__':
    main()
