import requests
import time
from typing import List, Dict

class BinanceClient:
    BASE_URL = "https://api.binance.com/api/v3"

    @staticmethod
    def get_historical_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 5000) -> List[Dict[str, float]]:
        url = f"{BinanceClient.BASE_URL}/klines"
        all_candles = []
        end_time = None
        
        print(f"Rozpoczęto pobieranie {limit} świec dla {symbol} (interwał: {interval}). Może to zająć chwilę...")
        
        while len(all_candles) < limit:
            current_limit = min(limit - len(all_candles), 1000)
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": current_limit
            }
            if end_time:
                params["endTime"] = end_time
                
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
                
            batch = []
            for kline in data:
                batch.append({
                    'timestamp_sec': int(kline[0]) // 1000,
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5])
                })
            
            all_candles.extend(batch)
            
            end_time = int(data[0][0]) - 1 
            time.sleep(0.1) 

        unique_candles = {c['timestamp_sec']: c for c in all_candles}
        sorted_candles = sorted(unique_candles.values(), key=lambda x: x['timestamp_sec'])
        
        return sorted_candles[-limit:]