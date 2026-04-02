from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV16(QCAlgorithm):
    """
    Rotation V16: The 50-Day Warning
    Uses a much faster moving average (50-day SMA on QQQ) to exit TQQQ before 
    the massive drawdowns that occur while waiting for the 200-day SMA to cross.
    """
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.SetCash(100_000)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 35),
            self.Rebalance,
        )

        tickers = ["QQQ", "TQQQ", "BIL"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi2_qqq = self.RSI(self.syms["QQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_qqq50 = self.SMA(self.syms["QQQ"],  50, Resolution.Daily)

        self.SetWarmUp(50, Resolution.Daily)

    def _pick(self) -> str:
        qqq_price  = self.Securities[self.syms["QQQ"]].Price

        bull = qqq_price > self.sma_qqq50.Current.Value
        panic = self.rsi2_qqq.Current.Value < 20

        if panic:
            # Always buy extreme panics
            return "TQQQ"

        if bull:
            # Uptrend
            return "TQQQ"
        else:
            # Downtrend: Hide in cash. The 50 SMA is fast enough to avoid 
            # the massive 40% drops that occur before the 200 SMA triggers.
            return "BIL"

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma_qqq50.IsReady or not self.rsi2_qqq.IsReady:
            return

        pick = self._pick()
        if not self.Portfolio[self.syms[pick]].Invested:
            self.Debug(f"[Rebalance] → Switching to {pick}")
            self.SetHoldings(self.syms[pick], 1.0, liquidateExistingHoldings=True)

    def OnData(self, data):
        pass
