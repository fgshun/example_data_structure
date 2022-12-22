import functools
import math
import operator
import random

import pytest

import sparsetable


@pytest.mark.parametrize('op', (max, min, operator.and_, operator.or_, math.gcd))
def test_sparsetable(op):
    r = random.Random()
    r.seed(0)
    seq = [r.randint(0, 127) for _ in range(100)]
    sparse_table = sparsetable.SparseTable(seq, op)

    for L in range(len(seq)):
        for R in range(L + 1, len(seq)):
            x = functools.reduce(op, seq[L:R])
            y = sparse_table.query(L, R)
            assert x == y