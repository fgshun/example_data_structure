"""Union Find Tree (Disjoint-set)

参考 - アルゴリズムロジック - Union-Find Tree を理解する！素集合系を扱うデータ構造
https://algo-logic.info/union-find-tree/

参考 - 重み付き Union-Find 木とそれが使える問題のまとめ、および、牛ゲーについて
@drken(株式会社NTTデータ数理システム)
https://qiita.com/drken/items/cce6fc5c579051e64fab#%E9%87%8D%E3%81%BF%E4%BB%98%E3%81%8D-union-find-%E6%9C%A8%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA
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



class WeightedUnionFindTree:
    """重み付き Union Find Tree
    
    重みは int に限らず、 アーベル群なら乗るとのことだが、
    とりあえずは int と決め打ちしておいて試作する。"""

    def __init__(self, n: int, weight_type=int) -> None:
        self.par = list(range(n))
        self.rank = [0] * n
        sum_unity = weight_type()
        self.diff_weight = [sum_unity] * n

    def find(self, x: int) -> int:
        par_x = self.par[x]
        if par_x == x:
            return x
        else:
            root = self.find(self.par[x])
            self.diff_weight[x] += self.diff_weight[par_x]
            self.par[x] = root
            return root
    
    def weight(self, x: int) -> int:
        self.find(x)
        return self.diff_weight[x]
    
    def diff(self, x: int, y: int) -> int:
        return self.weight(y) - self.weight(x)

    def unite(self, x: int, y: int, w: int) -> bool:
        w += self.weight(x)
        w -= self.weight(y)
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.rank[x] < self.rank[y]:
            x, y = y, x
            w = -w
        if self.rank[x] == self.rank[y]:
            self.rank[x] += 1
        self.par[y] = x
        self.diff_weight[y] = w
        return True

    def same(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def groups(self):
        result = [[] for _ in range(len(self.par))]
        for i in range(len(self.par)):
            result[self.find(i)].append(i)
        return filter(None, result)