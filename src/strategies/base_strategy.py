from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseStrategy(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate_signals(self, candles: List[Dict[str, float]]) -> List[int]:

        pass