from .base_strategy import BaseStrategy
from src.dsa.sliding_window import CircularSlidingWindow
from typing import List, Dict

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, short_window: int = 10, long_window: int = 50, use_ema: bool = False):
        name_prefix = "EMA" if use_ema else "SMA"
        super().__init__(f"{name_prefix} Crossover ({short_window}/{long_window})")
        self.short_window = short_window
        self.long_window = long_window
        self.use_ema = use_ema

    def generate_signals(self, candles: List[Dict[str, float]]) -> List[int]:
        signals = [0] * len(candles)
        if len(candles) < self.long_window:
            return signals

        short_q = CircularSlidingWindow(self.short_window)
        long_q = CircularSlidingWindow(self.long_window)
        
        prev_short_ma, prev_long_ma = None, None
        ema_short, ema_long = None, None
        k_short = 2 / (self.short_window + 1)
        k_long = 2 / (self.long_window + 1)

        for i, candle in enumerate(candles):
            price = candle['close']
            short_q.add(price)
            long_q.add(price)

            if i >= self.long_window:
                if self.use_ema:
                    if ema_short is None:
                        ema_short = short_q.get_sma()
                        ema_long = long_q.get_sma()
                    else:
                        ema_short = (price * k_short) + (ema_short * (1 - k_short))
                        ema_long = (price * k_long) + (ema_long * (1 - k_long))
                    current_short, current_long = ema_short, ema_long
                else:
                    current_short, current_long = short_q.get_sma(), long_q.get_sma()

                if prev_short_ma is not None and prev_long_ma is not None:
                    if prev_short_ma <= prev_long_ma and current_short > current_long:
                        signals[i] = 1
                    elif prev_short_ma >= prev_long_ma and current_short < current_long:
                        signals[i] = -1

                prev_short_ma, prev_long_ma = current_short, current_long

        return signals