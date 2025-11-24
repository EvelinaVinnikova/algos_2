class Node:
    def __init__(self, left=None, right=None, count=0):
        self.left = left
        self.right = right
        self.count = count


class PersistentSegmentTree:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.coords = sorted(set(arr))
        self.coord_to_idx = {val: i for i, val in enumerate(self.coords)}
        self.size = len(self.coords)
        self.roots = []
        self.root = None
        for i in range(self.n):
            self.root = self._update(self.root, 0, self.size - 1, self.coord_to_idx[arr[i]], 1)
            self.roots.append(self.root)

    def _update(self, node, start, end, idx, delta):
        if start == end:
            new_count = (node.count if node else 0) + delta
            return Node(count=new_count)

        mid = (start + end) // 2
        left_node = node.left if node else None
        right_node = node.right if node else None

        if idx <= mid:
            left_node = self._update(left_node, start, mid, idx, delta)
        else:
            right_node = self._update(right_node, mid + 1, end, idx, delta)

        left_count = left_node.count if left_node else 0
        right_count = right_node.count if right_node else 0

        return Node(left_node, right_node, left_count + right_count)

    def _query(self, node, start, end, l, r):
        if not node or r < start or end < l:
            return 0
        if l <= start and end <= r:
            return node.count
        mid = (start + end) // 2
        left_sum = self._query(node.left, start, mid, l, r) if node.left else 0
        right_sum = self._query(node.right, mid + 1, end, l, r) if node.right else 0
        return left_sum + right_sum

    def query_range_ge_k(self, l, r, k):
        """
        Возвращает количество элементов >= k в подмассиве arr[l:r+1]
        """
        left_idx = self._find_first_ge(k)
        if left_idx == -1:
            return 0

        root_r = self.roots[r] if r >= 0 else None
        root_l_minus_1 = self.roots[l - 1] if l > 0 else None

        count_r = self._query(root_r, 0, self.size - 1, left_idx, self.size - 1)
        count_l_minus_1 = self._query(root_l_minus_1, 0, self.size - 1, left_idx,
                                      self.size - 1) if root_l_minus_1 else 0

        return count_r - count_l_minus_1

    def _find_first_ge(self, k):
        """Находит индекс первого элемента >= k в coords"""
        left, right = 0, len(self.coords) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if self.coords[mid] >= k:
                result = mid
                right = mid - 1
            else:
                left = mid + 1
        return result



def test_persistent_segment_tree():
    # Тест 1: Все элементы одинаковые, k равно этому элементу
    arr1 = [2, 2, 2, 2, 2]
    pst1 = PersistentSegmentTree(arr1)
    assert pst1.query_range_ge_k(0, 4, 2) == 5, "Тест 1 провален: [2,2,2,2,2] >= 2 должно быть 5"

    # Тест 2: k больше всех элементов → ожидаем 0
    arr2 = [1, 3, 5, 7, 9]
    pst2 = PersistentSegmentTree(arr2)
    assert pst2.query_range_ge_k(0, 4, 10) == 0, "Тест 2 провален: нет элементов >= 10"

    # Тест 3: k совпадает с частью элементов
    arr3 = [10, 20, 30, 40, 50]
    pst3 = PersistentSegmentTree(arr3)
    assert pst3.query_range_ge_k(1, 3, 20) == 3, "Тест 3 провален: [20,30,40] >= 20 → 3 элемента"

    # Тест 4: Массив из одного элемента, k равен ему
    arr4 = [42]
    pst4 = PersistentSegmentTree(arr4)
    assert pst4.query_range_ge_k(0, 0, 42) == 1, "Тест 4 провален: [42] >= 42 → 1"


    # Ещё один тест: отрицательные числа
    arr5 = [-5, -2, 0, 3, 7]
    pst5 = PersistentSegmentTree(arr5)
    assert pst5.query_range_ge_k(0, 4, 0) == 3, "Тест 5 провален: [-5,-2,0,3,7] >= 0 → 3 элемента"

    print("Все тесты пройдены!")


test_persistent_segment_tree()
