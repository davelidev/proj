from AlgorithmImports import *


class Algo061(QCAlgorithm):
    """#61 — TQQQ + SMA150 (faster trend, may reduce DD further)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.s = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.s, 150, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.s),
                         self.TimeRules.AfterMarketOpen(self.s, 30), self.R)

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        in_trend = self.Securities[self.s].Price > self.sma.Current.Value
        invested = self.Portfolio[self.s].Invested
        if in_trend and not invested: self.SetHoldings(self.s, 1.0)
        elif not in_trend and invested: self.Liquidate(self.s)
