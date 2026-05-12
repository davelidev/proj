from AlgorithmImports import *


class Algo039(QCAlgorithm):
    """#39 — IBS extreme + max hold 3 days (avoid bag-holding through reversals)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(5, Resolution.Daily)
        self.entry_bar = None
        self.bar_count = 0
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        self.bar_count += 1
        bar = self.Securities[self.tqqq]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        invested = self.Portfolio[self.tqqq].Invested
        if not invested and ibs < 0.1:
            self.SetHoldings(self.tqqq, 1.0)
            self.entry_bar = self.bar_count
        elif invested:
            held = self.bar_count - (self.entry_bar or self.bar_count)
            if ibs > 0.9 or held >= 3:
                self.Liquidate(self.tqqq)
                self.entry_bar = None
