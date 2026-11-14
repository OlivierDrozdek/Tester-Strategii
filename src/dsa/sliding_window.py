from typing import Optional

class CircularSlidingWindow:

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Rozmiar okna musi być dodatni.")
        self.size = size
        self.buffer = [0.0] * size
        self.head = 0
        self.count = 0
        self.current_sum = 0.0

    def add(self, value: float) -> None:
        if self.count == self.size:
            self.current_sum -= self.buffer[self.head]
        else:
            self.count += 1
            
        self.buffer[self.head] = value
        self.current_sum += value
        self.head = (self.head + 1) % self.size

    def is_full(self) -> bool:
        return self.count == self.size

    def get_sma(self) -> Optional[float]:
        if not self.is_full():
            return None
        return self.current_sum / self.size

    def get_latest_values(self) -> list:
        if self.count < self.size:
            return self.buffer[:self.count]
        return self.buffer[self.head:] + self.buffer[:self.head]