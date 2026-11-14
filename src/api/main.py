from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from src.db.repository import CryptoRepository
from src.main import main as run_engine
import os

app = FastAPI(title="Tester Strategii", version="2.0")

static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))

@app.get("/")
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend index.html not found"}

@app.post("/api/run-backtest")
async def trigger_backtest(interval: str = "1h", limit: int = 5000):
    try:
        run_engine(interval=interval, limit=limit)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results/{symbol}")
async def get_backtest_results(symbol: str):
    repo = CryptoRepository()
    results = repo.get_latest_results(symbol=symbol)
    if not results:
        return []
    return [{
        "rank": i + 1,
        "strategy_name": r.strategy_name,
        "win_rate": r.win_rate,
        "pnl": r.pnl,
        "max_drawdown": r.max_drawdown,
        "trades_count": r.trades_count,
        "similarity_score": r.similarity_score
    } for i, r in enumerate(results)]