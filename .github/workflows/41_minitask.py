from typing import List


class SegmentTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)
        self.size = size

    def update(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index):
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & (-index)
        return s

class Solution:

    def countSmaller(self, nums: List[int]) -> List[int]:
        N = len(nums)
        if N == 0:
            return []
        sorted_unique_nums = sorted(list(set(nums)))
        rank_map = {val: i + 1 for i, val in enumerate(sorted_unique_nums)}

        M = len(sorted_unique_nums)
        bit = SegmentTree(M)

        counts = [0] * N
        for i in range(N - 1, -1, -1):
            num = nums[i]
            rank = rank_map[num]
            smaller_count = bit.query(rank - 1)
            counts[i] = smaller_count

            bit.update(rank, 1)

        return counts
