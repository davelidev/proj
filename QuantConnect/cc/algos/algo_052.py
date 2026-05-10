from AlgorithmImports import *


class Algo052(QCAlgorithm):
    """#52 — XLK (tech sector) trend on 200d SMA."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.xlk = self.AddEquity("XLK", Resolution.Daily).Symbol
        self.sma = self.SMA(self.xlk, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.xlk),
                         self.TimeRules.AfterMarketOpen(self.xlk, 30),
                         self.R)

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        in_trend = self.Securities[self.xlk].Price > self.sma.Current.Value
        invested = self.Portfolio[self.xlk].Invested
        if in_trend and not invested: self.SetHoldings(self.xlk, 1.0)
        elif not in_trend and invested: self.Liquidate(self.xlk)
