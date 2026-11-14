from sqlalchemy import Column, Integer, String, Float, BigInteger
from .connection import Base, SessionLocal
from typing import List, Dict, Any

class Candle(Base):
    __tablename__ = "candles"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True)
    timestamp_sec = Column(BigInteger, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class BacktestResult(Base):
    __tablename__ = "backtest_results"
    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String(50), index=True)
    symbol = Column(String(20), index=True)
    test_timestamp = Column(BigInteger)
    win_rate = Column(Float)
    pnl = Column(Float)
    max_drawdown = Column(Float)
    trades_count = Column(Integer)
    similarity_score = Column(Float, nullable=True)

class CryptoRepository:
    def __init__(self):
        self.db = SessionLocal()
        Base.metadata.create_all(bind=self.db.get_bind())

    def save_candles_bulk(self, symbol: str, candles_data: List[Dict[str, float]]):
        """Masowy zapis historii świec (szybszy niż pojedyncze inserty)."""
        objects = []
        for data in candles_data:
            objects.append(Candle(
                symbol=symbol,
                timestamp_sec=data['timestamp_sec'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                volume=data['volume']
            ))
        self.db.bulk_save_objects(objects)
        self.db.commit()

    def save_backtest_results(self, symbol: str, test_timestamp: int, results: List[Dict[str, Any]]):
        """Zapisuje wygenerowany ranking strategii."""
        objects = []
        for r in results:
            similarity = None
            if 'K-NN' in r['info']:
                try:
                    sim_str = r['info'].split('Podobieństwo: ')[1].replace('%)', '')
                    similarity = float(sim_str)
                except IndexError:
                    pass

            objects.append(BacktestResult(
                strategy_name=r['strategy_name'],
                symbol=symbol,
                test_timestamp=test_timestamp,
                win_rate=r['win_rate'],
                pnl=r['pnl'],
                max_drawdown=r['max_drawdown'],
                trades_count=r['trades_count'],
                similarity_score=similarity
            ))
        self.db.bulk_save_objects(objects)
        self.db.commit()
        
    def get_latest_results(self, symbol: str, limit: int = 5):
        """Pobiera najnowszy wygenerowany ranking z bazy danych dla UI."""
        return self.db.query(BacktestResult).filter(
            BacktestResult.symbol == symbol
        ).order_by(BacktestResult.test_timestamp.desc(), BacktestResult.win_rate.desc()).limit(limit).all()