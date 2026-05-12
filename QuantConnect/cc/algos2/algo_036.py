from AlgorithmImports import *


class Algo036(QCAlgorithm):
    """#36 — TQQQ Turn-of-Month: hold last 5 trading days + first 3 of month."""

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
        d = self.Time.day
        # Approximate: last 5 cal days + first 3 cal days
        in_window = d >= 25 or d <= 5
        invested = self.Portfolio[self.tqqq].Invested
        if in_window and not invested:
            self.SetHoldings(self.tqqq, 1.0)
        elif not in_window and invested:
            self.Liquidate(self.tqqq)
