
CREATE UNIQUE INDEX IF NOT EXISTS idx_candles_symbol_time ON candles(symbol, timestamp_sec);
CREATE INDEX IF NOT EXISTS idx_backtest_strategy ON backtest_results(strategy_name, symbol);