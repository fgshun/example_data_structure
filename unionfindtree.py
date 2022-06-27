"""Union Find Tree (Disjoint-set)

参考 - アルゴリズムロジック - Union-Find Tree を理解する！素集合系を扱うデータ構造
https://algo-logic.info/union-find-tree/
"""


class UnionFindTreeRank:
    def __init__(self, n: int) -> None:
        self.par = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    def unite(self, x: int, y: int) -> bool:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1
        return True

    def same(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def groups(self):
        result = [[] for _ in range(len(self.par))]
        for i in range(len(self.par)):
            result[self.find(i)].append(i)
        return filter(None, result)


class UnionFindTreeSize:
    def __init__(self, n: int) -> None:
        self.par = list(range(n))
        self._size = [1] * n

    def find(self, x: int) -> int:
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    def unite(self, x: int, y: int) -> bool:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self._size[x] < self._size[y]:
            self.par[x] = y
            self._size[y] += self._size[x]
        else:
            self.par[y] = x
            self._size[x] += self._size[y]
        return True

    def same(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def size(self, x: int) -> int:
        return self._size[self.find(x)]

    def groups(self):
        result = [[] for _ in range(len(self.par))]
        for i in range(len(self.par)):
            result[self.find(i)].append(i)
        return filter(None, result)

    # def groups(self):
    #     result = {}
    #     for i in range(len(self.par)):
    #         result.setdefault(self.find(i), []).append(i)
    #     return result.values()


UnionFindTree = UnionFindTreeRank
