from typing import List

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        
        class UnionFind:
            def __init__(self, n):
                self.parent = list(range(n + 1))
                self.rank = [0] * (n + 1)

            def find(self, i: int) -> int:
                """Находит корень для i с использованием сжатия путей"""
                if self.parent[i] == i:
                    return i
                
                self.parent[i] = self.find(self.parent[i])
                return self.parent[i]

            def union(self, i: int, j: int) -> bool:
                """Объединяет множества i и j по рангу"""
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
        
        num_nodes = len(edges)
        uf = UnionFind(num_nodes)

        for u, v in edges:
            if not uf.union(u, v):
                return [u, v]        
        return []
