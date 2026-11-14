from typing import Any, Optional, List, Tuple

class TimeSeriesCache:

    def __init__(self, initial_capacity: int = 4096):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = 0.75
        self.buckets: List[List[Tuple[int, Any]]] = [[] for _ in range(self.capacity)]

    def _hash(self, timestamp: int) -> int:
        timestamp ^= (timestamp >> 20) ^ (timestamp >> 12)
        return (timestamp ^ (timestamp >> 7) ^ (timestamp >> 4)) % self.capacity

    def put(self, timestamp: int, data: Any) -> None:
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

        idx = self._hash(timestamp)
        for i, (ts, _) in enumerate(self.buckets[idx]):
            if ts == timestamp:
                self.buckets[idx][i] = (timestamp, data)
                return
        
        self.buckets[idx].append((timestamp, data))
        self.size += 1

    def get(self, timestamp: int) -> Optional[Any]:
        idx = self._hash(timestamp)
        for ts, data in self.buckets[idx]:
            if ts == timestamp:
                return data
        return None

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for ts, data in bucket:
                self.put(ts, data)