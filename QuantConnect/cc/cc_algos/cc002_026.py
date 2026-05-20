from AlgorithmImports import *


class Algo009(QCAlgorithm):
    """#9 — TQQQ self-SMA150."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma  = self.SMA(self.tqqq, 150, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        in_trend = self.Securities[self.tqqq].Price > self.sma.Current.Value
        invested = self.Portfolio[self.tqqq].Invested
        if in_trend and not invested: self.SetHoldings(self.tqqq, 1.0)
        elif not in_trend and invested: self.Liquidate(self.tqqq)
