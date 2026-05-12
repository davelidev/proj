from AlgorithmImports import *


class Algo050(QCAlgorithm):
    """#50 — TQQQ single stock, hold and rebalance."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.s = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(5, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.s),
                         self.TimeRules.AfterMarketOpen(self.s, 30),
                         self.R)

    def R(self):
        if self.IsWarmingUp: return
        if not self.Portfolio[self.s].Invested:
            self.SetHoldings(self.s, 1.0)
