from typing import List, Dict, Any

class PerformanceMetrics:
    @staticmethod
    def calculate(trades_pnl: List[float], similarity_context: str = "") -> Dict[str, Any]:
        if not trades_pnl:
            return {
                'win_rate': 0.0,
                'pnl': 0.0,
                'max_drawdown': 0.0,
                'trades_count': 0,
                'info': "Brak sygnałów – za mała zmienność. " + similarity_context
            }

        wins = sum(1 for t in trades_pnl if t > 0)
        win_rate = (wins / len(trades_pnl)) * 100
        pnl = sum(trades_pnl)
        
        peak = 0.0
        current_eq = 0.0
        max_dd = 0.0
        
        for trade in trades_pnl:
            current_eq += trade
            if current_eq > peak:
                peak = current_eq
            dd = peak - current_eq
            if dd > max_dd:
                max_dd = dd

        return {
            'win_rate': round(win_rate, 2),
            'pnl': round(pnl, 2),
            'max_drawdown': round(max_dd, 2),
            'trades_count': len(trades_pnl),
            'info': similarity_context or "Baza bazowa"
        }