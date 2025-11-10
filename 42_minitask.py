from typing import List

MOD = 10**9 + 7

class FenwickTree:
    def __init__(self, n: int):
        self.len = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        while i <= self.len:
            self.tree[i] += delta
            i += (i &(-i))

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= (i &(-i))
        return s

class Solution:
    def createSortedArray(self, instructions: List[int]) -> int:
        if not instructions:
            return 0
        MAXV = max(instructions) + 2
        bit = FenwickTree(MAXV)
        ans = 0

        for i, x in enumerate(instructions):
            less = bit.sum(x - 1)
            less_or_equal = bit.sum(x)
            greater = i - less_or_equal
            ans = (ans + min(less, greater)) % MOD
            bit.add(x, 1)
        return ans
