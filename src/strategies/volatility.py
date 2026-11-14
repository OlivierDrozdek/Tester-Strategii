from .base_strategy import BaseStrategy
from src.dsa.segment_tree import MinMaxSegmentTree
from src.dsa.sliding_window import CircularSlidingWindow
from typing import List, Dict
import math

class BreakoutStrategy(BaseStrategy):
    def __init__(self, lookback_period: int = 20):
        super().__init__(f"Support/Resistance Breakout ({lookback_period})")
        self.lookback = lookback_period

    def generate_signals(self, candles: List[Dict[str, float]]) -> List[int]:
        signals = [0] * len(candles)
        if len(candles) <= self.lookback:
            return signals

        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        
        tree_highs = MinMaxSegmentTree(highs)
        tree_lows = MinMaxSegmentTree(lows)

        for i in range(self.lookback, len(candles)):
            _, local_max = tree_highs.query(i - self.lookback, i - 1)
            local_min, _ = tree_lows.query(i - self.lookback, i - 1)
            
            current_close = candles[i]['close']
            if current_close > local_max:
                signals[i] = 1 
            elif current_close < local_min:
                signals[i] = -1 

        return signals

class BollingerBandsStrategy(BaseStrategy):
    def __init__(self, period: int = 20, std_dev_multiplier: float = 2.0):
        super().__init__("Bollinger Bands")
        self.period = period
        self.multiplier = std_dev_multiplier

    def generate_signals(self, candles: List[Dict[str, float]]) -> List[int]:
        signals = [0] * len(candles)
        window = CircularSlidingWindow(self.period)
        
        for i, candle in enumerate(candles):
            price = candle['close']
            window.add(price)
            
            if window.is_full():
                sma = window.get_sma()
                vals = window.get_latest_values()
                variance = sum((x - sma) ** 2 for x in vals) / self.period
                std_dev = math.sqrt(variance)
                
                upper_band = sma + (self.multiplier * std_dev)
                lower_band = sma - (self.multiplier * std_dev)
                
                if price < lower_band:
                    signals[i] = 1
                elif price > upper_band:
                    signals[i] = -1
                    
        return signals