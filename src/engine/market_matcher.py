import math
from typing import List, Dict, Any, Tuple

class MarketMatcherKNN:
    def __init__(self, feature_window: int = 20, k_neighbors: int = 5):
        self.feature_window = feature_window
        self.k_neighbors = k_neighbors

    def _extract_features(self, prices: List[float]) -> Tuple[float, float]:
        if len(prices) < 2:
            return 0.0, 0.0
            
        mean_p = sum(prices) / len(prices)
        variance = sum((p - mean_p)**2 for p in prices) / len(prices)
        volatility = math.sqrt(variance) / mean_p if mean_p != 0 else 0
        
        trend = (prices[-1] - prices[0]) / prices[0] if prices[0] != 0 else 0
        
        return volatility, trend

    def find_similar_market_conditions(self, all_candles: List[Dict], current_idx: int) -> List[Dict[str, Any]]:
        if current_idx < self.feature_window * 2:
            return []

        prices = [c['close'] for c in all_candles]
        current_prices = prices[current_idx - self.feature_window : current_idx]
        curr_vol, curr_trend = self._extract_features(current_prices)
        
        distances = []
        for i in range(self.feature_window, current_idx - self.feature_window):
            hist_prices = prices[i - self.feature_window : i]
            hist_vol, hist_trend = self._extract_features(hist_prices)
            
            dist = math.sqrt((curr_vol - hist_vol)**2 + (curr_trend - hist_trend)**2)
            
            similarity = max(0.0, 100.0 - (dist * 1000))
            
            distances.append({
                'end_idx': i,
                'distance': dist,
                'similarity_score': similarity
            })

        distances.sort(key=lambda x: x['distance'])
        return distances[:self.k_neighbors]