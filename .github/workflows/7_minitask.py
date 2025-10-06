from collections import defaultdict
from math import factorial


class TreeTopoSort:
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(list)
        self.size = [0] * (n + 1)
        self.dp = [0] * (n + 1)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def count_topological_sorts(self, root=1):
        self._dfs(root)
        return self.dp[root]

    def _dfs(self, v):
        children = self.graph[v]

        if not children:
            self.size[v] = 1
            self.dp[v] = 1
            return

        self.size[v] = 1
        self.dp[v] = 1

        for child in children:
            self._dfs(child)
            self.size[v] += self.size[child]

        # Вычисляем dp[v]
        # Формула: (size[v]-1)! / произведение size[child]! для всех детей
        # умноженное на произведение dp[child]

        numerator = factorial(self.size[v] - 1)
        denominator = 1

        for child in children:
            denominator *= factorial(self.size[child])
            self.dp[v] *= self.dp[child]

        self.dp[v] *= numerator // denominator


#     1
#    / \
#   2   3
#  /
# 4
print("First example:")
tree1 = TreeTopoSort(4)
tree1.add_edge(1, 2)
tree1.add_edge(1, 3)
tree1.add_edge(2, 4)
result1 = tree1.count_topological_sorts(1)
print(f"Number of topological sorts: {result1}")
print("Possible sorts: [1,2,3,4], [1,2,4,3], [1,3,2,4]")

#  1 -> 2 -> 3 -> 4
print("Second examlpe:")
tree2 = TreeTopoSort(4)
tree2.add_edge(1, 2)
tree2.add_edge(2, 3)
tree2.add_edge(3, 4)
result2 = tree2.count_topological_sorts(1)
print(f"Number of topological sorts: {result2}")
print("Only sort: [1,2,3,4]")

#     1
#   / | \
#  2  3  4
print("Third example:")
tree3 = TreeTopoSort(4)
tree3.add_edge(1, 2)
tree3.add_edge(1, 3)
tree3.add_edge(1, 4)
result3 = tree3.count_topological_sorts(1)
print(f"Number of topological sorts: {result3}")
print("3! = 6 ways to align children after root")

#       1
#      / \
#     2   3
#    / \   \
#   4   5   6
print("Fourth example:")
tree4 = TreeTopoSort(6)
tree4.add_edge(1, 2)
tree4.add_edge(1, 3)
tree4.add_edge(2, 4)
tree4.add_edge(2, 5)
tree4.add_edge(3, 6)
result4 = tree4.count_topological_sorts(1)
print(f"Number of topological sorts: {result4}")
