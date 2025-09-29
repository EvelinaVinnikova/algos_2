class Solution:
    def numTrees(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        k = 2
        while k <= n:
            total = 0
            i = 1
            while i <= k:
                left = i - 1
                right = k - i
                total += dp[left] * dp[right]
                i += 1
            dp[k] = total
            k += 1

        return dp[n]
