from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, period=14, oversold=30, overbought=70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        self.name = f"RSI ({period})"

    def generate_signals(self, candles):
        closes = [c['close'] for c in candles]
        signals = [0] * len(closes)
        
        if len(closes) < self.period + 1:
            return signals

        gains, losses = [], []
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i-1]
            gains.append(max(diff, 0))
            losses.append(max(-diff, 0))

        avg_gain = sum(gains[:self.period]) / self.period
        precision_loss = sum(losses[:self.period]) / self.period

        for i in range(self.period, len(closes)):
            diff = closes[i] - closes[i-1]
            gain = max(diff, 0)
            loss = max(-diff, 0)
            
            avg_gain = (avg_gain * (self.period - 1) + gain) / self.period
            precision_loss = (precision_loss * (self.period - 1) + loss) / self.period

            if precision_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / precision_loss
                rsi = 100 - (100 / (1 + rs))

            idx = i + 1
            if idx < len(signals):
                if rsi < self.oversold:
                    signals[idx] = 1
                elif rsi > self.overbought:
                    signals[idx] = -1

        return signals


class MACDStrategy(BaseStrategy):
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal_period = signal
        self.name = f"MACD ({fast}/{slow}/{signal})"

    def generate_signals(self, candles):
        closes = [c['close'] for c in candles]
        signals = [0] * len(closes)
        
        if len(closes) < self.slow + self.signal_period:
            return signals

        def calculate_ema(data, period):
            ema = []
            multiplier = 2 / (period + 1)
            for i, val in enumerate(data):
                if i == 0:
                    ema.append(val)
                else:
                    ema.append((val - ema[-1]) * multiplier + ema[-1])
            return ema

        ema_fast = calculate_ema(closes, self.fast)
        ema_slow = calculate_ema(closes, self.slow)
        
        macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
        signal_line = calculate_ema(macd_line, self.signal_period)
        
        histogram = [m - s for m, s in zip(macd_line, signal_line)]

        for i in range(1, len(closes)):
            if histogram[i-1] <= 0 and histogram[i] > 0:
                signals[i] = 1
            elif histogram[i-1] >= 0 and histogram[i] < 0:
                signals[i] = -1

        return signals