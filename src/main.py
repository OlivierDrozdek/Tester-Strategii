import time
from src.config import settings
from src.engine.backtester import BacktestEngine
from src.strategies.crossovers import MovingAverageCrossover
from src.strategies.oscillators import RSIStrategy, MACDStrategy
from src.strategies.volatility import BollingerBandsStrategy, BreakoutStrategy
from src.dsa.sorting import rank_strategies
from src.db.binance import BinanceClient
from src.db.repository import CryptoRepository

def main(interval: str = "1h", limit: int = 5000):
    symbol = "BTCUSDT"
    candles = BinanceClient.get_historical_klines(symbol=symbol, interval=interval, limit=limit)
    
    strategies = [
        MovingAverageCrossover(short_window=10, long_window=50),
        RSIStrategy(period=14),
        MACDStrategy(),
        BollingerBandsStrategy(period=20),
        BreakoutStrategy(lookback_period=20)
    ]
    
    engine = BacktestEngine(candles, strategies)
    results = engine.run_backtest()
    ranked_results = rank_strategies(results)
    
    repo = CryptoRepository()
    repo.save_candles_bulk(symbol, candles)
    repo.save_backtest_results(symbol, int(time.time()), ranked_results)
    return ranked_results

if __name__ == "__main__":
    main()