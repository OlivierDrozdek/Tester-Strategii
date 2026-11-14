from typing import List, Tuple, Union

class MinMaxSegmentTree:

    def __init__(self, data: List[float]):
        self.n = len(data)
        if self.n == 0:
            raise ValueError("Dane wejściowe nie mogą być puste.")
            
        self.tree_min = [float('inf')] * (4 * self.n)
        self.tree_max = [float('-inf')] * (4 * self.n)
        self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[float], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree_min[node] = data[start]
            self.tree_max[node] = data[start]
            return

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)

        self.tree_min[node] = min(self.tree_min[left_child], self.tree_min[right_child])
        self.tree_max[node] = max(self.tree_max[left_child], self.tree_max[right_child])

    def query(self, left: int, right: int) -> Tuple[float, float]:
 
        if left > right or left < 0 or right >= self.n:
            raise IndexError("Nieprawidłowy przedział zapytania.")
        return self._query_util(0, 0, self.n - 1, left, right)

    def _query_util(self, node: int, start: int, end: int, l: int, r: int) -> Tuple[float, float]:
        if r < start or end < l:
            return float('inf'), float('-inf')
            
        if l <= start and end <= r:
            return self.tree_min[node], self.tree_max[node]
            
        mid = (start + end) // 2
        left_min, left_max = self._query_util(2 * node + 1, start, mid, l, r)
        right_min, right_max = self._query_util(2 * node + 2, mid + 1, end, l, r)
        
        return min(left_min, right_min), max(left_max, right_max)