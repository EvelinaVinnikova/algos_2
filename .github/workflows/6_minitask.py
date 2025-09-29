from typing import List
class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m = len(dungeon) # строки
        n = len(dungeon[0]) # столбцы
        min_hp_matrix = [[1] * n for _ in range(m)] # в каждой клетке min hp для того чтобы попав в нее не умереть
        for i in range(m-1, -1, -1):
            for j in range(n-1,  -1, -1):
                if i == m-1 and j == n-1:
                    min_hp_matrix[i][j] -= dungeon[i][j]
                elif i == m-1:
                    min_hp_matrix[i][j] = min_hp_matrix[i][j+1] - dungeon[i][j]
                elif j == n-1:
                    min_hp_matrix[i][j] = min_hp_matrix[i+1][j] - dungeon[i][j]
                else:
                    min_hp_matrix[i][j] = min(min_hp_matrix[i+1][j], min_hp_matrix[i][j+1]) - dungeon[i][j]
                if min_hp_matrix[i][j] < 1:
                    min_hp_matrix[i][j] = 1
        return min_hp_matrix[0][0]
