from AlgorithmImports import *


class Algo012(QCAlgorithm):
    """#12 — Static 50/50 TQQQ/TLT, monthly rebalance (risk parity-ish)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.tlt  = self.AddEquity("TLT",  Resolution.Daily).Symbol
        self.SetWarmUp(20, Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        self.SetHoldings(self.tqqq, 0.5)
        self.SetHoldings(self.tlt,  0.5)
