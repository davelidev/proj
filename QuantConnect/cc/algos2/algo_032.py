from AlgorithmImports import *


class Algo032(QCAlgorithm):
    """#32 — IBS<0.05 (extreme oversold), exit IBS>0.9. Lower freq, very high quality."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(5, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        bar = self.Securities[self.tqqq]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        invested = self.Portfolio[self.tqqq].Invested
        if not invested and ibs < 0.05:
            self.SetHoldings(self.tqqq, 1.0)
        elif invested and ibs > 0.9:
            self.Liquidate(self.tqqq)
