from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV10(QCAlgorithm):
    """
    Rotation V10: Momentum Sniper
    Combines the safety gates of V9 (which reduced drawdown to 44%) 
    with a Relative Strength momentum selector for the Bull leg to push 
    the CAGR back over 100%.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("SPY"),
            self.TimeRules.AfterMarketOpen("SPY", 35),
            self.Rebalance,
        )

        self.bull_assets = ["TQQQ", "SOXL", "TECL"]
        tickers = ["SPY", "QQQ", "SQQQ", "BIL"] + self.bull_assets
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi2_qqq = self.RSI(self.syms["QQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy200 = self.SMA(self.syms["SPY"], 200, Resolution.Daily)
        self.sma_tqqq20 = self.SMA(self.syms["TQQQ"], 20, Resolution.Daily)

        # 20-day Momentum for relative strength rotation during bull markets
        self.mom = {t: self.MOMP(self.syms[t], 20, Resolution.Daily) for t in self.bull_assets}

        self.SetWarmUp(200, Resolution.Daily)

    def _get_best_bull(self):
        ready = {t: ind.Current.Value for t, ind in self.mom.items() if ind.IsReady}
        if not ready: 
            return "TQQQ"
        return max(ready, key=ready.get)

    def _pick(self) -> str:
        spy_price = self.Securities[self.syms["SPY"]].Price
        tqqq_price = self.Securities[self.syms["TQQQ"]].Price

        bull = spy_price > self.sma_spy200.Current.Value
        tqqq_below_20sma = tqqq_price < self.sma_tqqq20.Current.Value
        
        # Slightly tighter panic trigger (15 instead of 20) to ensure extreme oversold
        panic = self.rsi2_qqq.Current.Value < 15

        if bull:
            if tqqq_below_20sma:
                if panic:
                    return self._get_best_bull()
                return "QQQ"
            return self._get_best_bull()
        else:
            # Bear Market
            if panic:
                return "TQQQ" # Safer than SOXL in a bear panic bounce
            if tqqq_below_20sma:
                return "SQQQ"
            return "BIL" # Bear market rally, sit in cash
            
    def Rebalance(self):
        if (self.IsWarmingUp 
            or not self.sma_spy200.IsReady 
            or not self.rsi2_qqq.IsReady):
            return
            
        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.Debug(f"[Rebalance] → Switching to {pick} (RSI: {self.rsi2_qqq.Current.Value:.2f})")
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
