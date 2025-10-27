from typing import List


class NumArray(object):
    def __init__(self, nums: List[int]):
        self.N = len(nums)
        if self.N == 0:
            self.tree = []
            return
        self.nums = nums

        self.tree = [0] * (4 * self.N)
        self.build(1, 0, self.N - 1)

    def build(self, v: int, tl: int, tr: int):
        if tl == tr:
            self.tree[v] = self.nums[tl]
        else:
            tm = (tl + tr) // 2
            self.build(2 * v, tl, tm)
            self.build(2 * v + 1, tm + 1, tr)

            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def update_tree(self, v: int, tl: int, tr: int, pos: int, new_val: int):
        if tl == tr:
            self.tree[v] = new_val
        else:
            tm = (tl + tr) // 2

            if pos <= tm:
                self.update_tree(2 * v, tl, tm, pos, new_val)
            else:
                self.update_tree(2 * v + 1, tm + 1, tr, pos, new_val)
            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query_sum(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        if l <= tl and tr <= r:
            return self.tree[v]

        if tl > r or tr < l:
            return 0

        tm = (tl + tr) // 2

        sum_left = self.query_sum(2 * v, tl, tm, l, r)
        sum_right = self.query_sum(2 * v + 1, tm + 1, tr, l, r)

        return sum_left + sum_right

    def update(self, index: int, val: int):
        if self.N == 0: return
        self.nums[index] = val
        self.update_tree(1, 0, self.N - 1, index, val)

    def sumRange(self, left: int, right: int) -> int:
        if self.N == 0: return 0
        return self.query_sum(1, 0, self.N - 1, left, right)
