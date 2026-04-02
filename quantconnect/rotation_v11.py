from datetime import datetime, timedelta
from AlgorithmImports import *

class RotationStrategyV11(QCAlgorithm):
    """
    Rotation V11: The QQQ Champion
    Combines the extreme dip-buying alpha of the 'Champion' strategy (rsi_rebalance.py)
    with a structural core holding.
    - Bull Market: Hold QQQ. On dips (RSI2 < 25), sprint to TQQQ.
    - Bear Market: Hold Cash. On panics (RSI2 < 25), sprint to TQQQ for the bounce.
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

        tickers = ["SPY", "QQQ", "TQQQ", "BIL"]
        self.syms = {t: self.AddEquity(t, Resolution.Daily).Symbol for t in tickers}

        self.rsi2_qqq = self.RSI(self.syms["QQQ"], 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma_spy200 = self.SMA(self.syms["SPY"], 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

    def _pick(self) -> str:
        spy_price = self.Securities[self.syms["SPY"]].Price
        bull = spy_price > self.sma_spy200.Current.Value
        dip = self.rsi2_qqq.Current.Value < 25

        if dip:
            return "TQQQ" # Aggressive sprint on any dip

        if bull:
            return "QQQ"  # Core holding during bull regimes
        else:
            return "BIL"  # Core holding during bear regimes
            
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
