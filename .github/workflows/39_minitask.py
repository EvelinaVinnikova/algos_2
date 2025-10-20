from typing import Optional
import random


class Node:
    def __init__(self, value):
        self.value = value
        self.priority = random.randint(0, 10 ** 18)
        self.size = 1
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.sum_value = value

    def updateData(self):
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        self.size = left_size + right_size + 1

        left_sum = self.left.sum_value if self.left else 0
        right_sum = self.right.sum_value if self.right else 0
        self.sum_value = left_sum + right_sum + self.value

    def getNodeSize(self):
        return self.size if self else 0


def splitBySize(node: Optional[Node], size: int) -> tuple[Optional[Node], Optional[Node]]:
    if not node:
        return None, None
    left_size = node.left.size if node.left else 0

    if size <= left_size:
        L, R = splitBySize(node.left, size)
        node.left = R
        node.updateData()
        return L, node
    else:
        L, R = splitBySize(node.right, size - left_size - 1)
        node.right = L
        node.updateData()
        return node, R


def merge(t1: Optional[Node], t2: Optional[Node]) -> Optional[Node]:
    if not t1: return t2
    if not t2: return t1
    if t1.priority > t2.priority:
        t1.right = merge(t1.right, t2)
        t1.updateData()
        return t1
    else:
        t2.left = merge(t1, t2.left)
        t2.updateData()
        return t2


class ImplicitCartesiaTree:
    def __init__(self):
        self.root: Optional[Node] = None

    def insert(self, pos: int, value: int):
        new_node = Node(value)
        t1, t_rest = splitBySize(self.root, pos)
        self.root = merge(merge(t1, new_node), t_rest)

    def erase(self, pos: int):
        if not self.root:
            return

        t1, t_rest = splitBySize(self.root, pos - 1)
        if not t_rest:
            self.root = t1
            return

        t_mid, t_right = splitBySize(t_rest, 1)
        self.root = merge(t1, t_right)

    def get(self, pos: int) -> Optional[int] | None:
        if not self.root:
            return None
        t1, t_rest = splitBySize(self.root, pos - 1)
        t_mid, t2 = splitBySize(t_rest, 1)

        result_value = t_mid.value if t_mid else None

        self.root = merge(merge(t1, t_mid), t2)
        return result_value

    def summ(self, from_pos: int, to_pos: int) -> int:
        if not self.root or from_pos > to_pos:
            return 0

        total_size = self.root.getNodeSize()
        if from_pos < 1 or to_pos > total_size:
            print("Attention: The given value range crosses tree limits.")
            from_pos = max(1, from_pos)
            to_pos = min(total_size, to_pos)
            if from_pos > to_pos: return 0

        t1, t23 = splitBySize(self.root, from_pos - 1)

        range_size = to_pos - from_pos + 1
        t2, t3 = splitBySize(t23, range_size)

        result_sum = t2.sum_value if t2 else 0

        self.root = merge(merge(t1, t2), t3)
        return result_sum


# --- Тесты ---
tree = ImplicitCartesiaTree()
values = [10, 20, 30, 40, 50]

for i, val in enumerate(values):
    tree.insert(i, val)

assert tree.root.size == 5, f"Ошибка размера: Ожидалось 5, получили {tree.root.size}"

# 2. Тест Get
assert tree.get(1) == 10, f"Ошибка get(1): Ожидалось 10, получили {tree.get(1)}"
assert tree.get(3) == 30, f"Ошибка get(3): Ожидалось 30, получили {tree.get(3)}"
assert tree.get(5) == 50, f"Ошибка get(5): Ожидалось 50, получили {tree.get(5)}"
assert tree.root.size == 5, "Ошибка: Размер после get неверный."


# 3. Тест Summ
assert tree.summ(1, 5) == 150, f"Ошибка summ(1, 5): Ожидалось 150, получили {tree.summ(1, 5)}"
assert tree.summ(2, 4) == 90, f"Ошибка summ(2, 4): Ожидалось 90, получили {tree.summ(2, 4)}"
assert tree.summ(5, 5) == 50, f"Ошибка summ(5, 5): Ожидалось 50, получили {tree.summ(5, 5)}"
assert tree.root.size == 5, "Ошибка: Размер после summ неверный."


# # 4. Тест Erase
tree.erase(3)  # Удаляем 30. Остается [10, 20, 40, 50]
assert tree.root.size == 4, f"Ошибка размера после erase: Ожидалось 4, получили {tree.root.size}"
assert tree.get(3) == 40, f"Ошибка get после erase: Ожидалось 40, получили {tree.get(3)}"
assert tree.summ(1, 4) == 120, f"Ошибка summ после erase: Ожидалось 120, получили {tree.summ(1, 4)}"
