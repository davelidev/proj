from AlgorithmImports import *


class Algo023(QCAlgorithm):
    """#23 — TQQQ 3-day-down MR. Buy after 3 consecutive down days, exit on 1st up day."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(10, Resolution.Daily)
        self.history = []
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp: return
        bar = self.Securities[self.tqqq]
        c = bar.Close
        if c <= 0: return
        self.history.append(c)
        if len(self.history) > 5:
            self.history = self.history[-5:]
        if len(self.history) < 4: return

        # last 3 closes lower than each previous?
        h = self.history
        three_down = h[-1] < h[-2] < h[-3] < h[-4]
        invested = self.Portfolio[self.tqqq].Invested
        if not invested and three_down:
            self.SetHoldings(self.tqqq, 1.0)
        elif invested and h[-1] > h[-2]:
            self.Liquidate(self.tqqq)
