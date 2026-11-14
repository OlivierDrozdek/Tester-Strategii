from src.engine.market_matcher import MarketMatcherKNN
from src.engine.metrics import PerformanceMetrics
from src.strategies.base_strategy import BaseStrategy
from typing import List, Dict, Any

class BacktestEngine:
    def __init__(self, candles: List[Dict], strategies: List[BaseStrategy]):
        self.candles = candles
        self.strategies = strategies
        self.matcher = MarketMatcherKNN()

    def run_backtest(self) -> List[Dict[str, Any]]:
        results = []
        for strategy in self.strategies:
            signals = strategy.generate_signals(self.candles)
            trades_pnl = []
            
            entry_price = 0.0
            for i, sig in enumerate(signals):
                current_price = self.candles[i]['close']
                if sig == 1 and entry_price == 0.0:
                    entry_price = current_price
                elif sig == -1 and entry_price > 0.0:
                    trades_pnl.append(current_price - entry_price)
                    entry_price = 0.0

            similarity_context = ""
            if len(trades_pnl) == 0:
                current_idx = len(self.candles) - 1
                neighbors = self.matcher.find_similar_market_conditions(self.candles, current_idx)
                
                if neighbors:
                    avg_sim = sum(n['similarity_score'] for n in neighbors) / len(neighbors)
                    similarity_context = f"Aproksymacja z historii K-NN (Podobieństwo: {avg_sim:.1f}%)"
                else:
                    similarity_context = "Zbyt krótka historia do wyznaczenia K-NN."

            metrics = PerformanceMetrics.calculate(trades_pnl, similarity_context)
            metrics['strategy_name'] = strategy.name
            results.append(metrics)

        return results