from AlgorithmImports import *


class Algo022(QCAlgorithm):
    """#22 — TQQQ Bollinger Band MR (20, 2). Buy at lower band, sell at middle."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bb   = self.BB(self.tqqq, 20, 2.0, MovingAverageType.Simple, Resolution.Daily)
        self.SetWarmUp(30, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.bb.IsReady: return
        px = self.Securities[self.tqqq].Price
        invested = self.Portfolio[self.tqqq].Invested
        if not invested and px <= self.bb.LowerBand.Current.Value:
            self.SetHoldings(self.tqqq, 1.0)
        elif invested and px >= self.bb.MiddleBand.Current.Value:
            self.Liquidate(self.tqqq)
