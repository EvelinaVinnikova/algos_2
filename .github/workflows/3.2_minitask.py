from typing import List

class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent = [0] * (n + 1)
        candidate1, candidate2 = None, None

        for u, v in edges:
            if parent[v] != 0:
                candidate1 = [parent[v], v]
                candidate2 = [u, v]
                break
            parent[v] = u
            
        class UnionFind:
            def __init__(self, n: int):
                self.parent = list(range(n + 1))
                self.rank = [0] * (n + 1)

            def find(self, i: int) -> int:
                """
                Находит корень множества для элемента i с помощью сжатия путей
                """
                if self.parent[i] == i:
                    return i
                self.parent[i] = self.find(self.parent[i])
                return self.parent[i]

            def union(self, i: int, j: int) -> bool:
                """
                Объединяет множества, содержащие i и j по рангу
                Возвращает False, если i и j уже находятся в одном множестве => цикл
                """
                root_i = self.find(i)
                root_j = self.find(j)
                if root_i == root_j:
                    return False
                
                if self.rank[root_i] < self.rank[root_j]:
                    self.parent[root_i] = root_j
                elif self.rank[root_i] > self.rank[root_j]:
                    self.parent[root_j] = root_i
                else:
                    self.parent[root_j] = root_i
                    self.rank[root_i] += 1
                return True

        uf = UnionFind(n)
        
        for u, v in edges:
            if [u, v] == candidate2:
                continue
            
            if not uf.union(u, v):
                if candidate1 is None:
                    return [u, v]
                else:
                    return candidate1

        return candidate2
