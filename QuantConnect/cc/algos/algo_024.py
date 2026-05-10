from AlgorithmImports import *


class Algo024(QCAlgorithm):
    """#24 — TQQQ Connors RSI-style: cumulative RSI(2) two-day buy."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi  = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(20, Resolution.Daily)
        self.prev_rsi = None
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi.IsReady: return
        cur = self.rsi.Current.Value
        prev = self.prev_rsi
        invested = self.Portfolio[self.tqqq].Invested
        # Cumulative entry: 2 consecutive RSI(2) < 35 (Larry Connors variant)
        if not invested and prev is not None and prev < 35 and cur < 35:
            self.SetHoldings(self.tqqq, 1.0)
        elif invested and cur > 65:
            self.Liquidate(self.tqqq)
        self.prev_rsi = cur
