from AlgorithmImports import *


class Algo054(QCAlgorithm):
    """#54 — TQQQ buy on first up day after 2 down days, exit on first down day."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.t = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.SetWarmUp(5, Resolution.Daily)
        self.history = []
        self.Schedule.On(self.DateRules.EveryDay(self.t),
                         self.TimeRules.AfterMarketOpen(self.t, 30),
                         self.R)

    def R(self):
        if self.IsWarmingUp: return
        c = self.Securities[self.t].Close
        if c <= 0: return
        self.history.append(c)
        if len(self.history) > 5: self.history = self.history[-5:]
        if len(self.history) < 4: return
        h = self.history
        # 2 down days then 1 up
        two_down_then_up = h[-2] < h[-3] < h[-4] and h[-1] > h[-2]
        invested = self.Portfolio[self.t].Invested
        if not invested and two_down_then_up:
            self.SetHoldings(self.t, 1.0)
        elif invested and h[-1] < h[-2]:
            self.Liquidate(self.t)
