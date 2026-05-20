from AlgorithmImports import *


class Algo009(QCAlgorithm):
    """#009 — 8 3×-leveraged ETFs equal-weighted, rebalanced monthly. No market timing."""

    TICKERS = ["TQQQ", "SOXL", "TECL", "UPRO", "FAS", "TNA", "CURE", "ERX"]

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.syms = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.TICKERS]
        self.SetWarmUp(5, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.syms[0]),
            self.TimeRules.AfterMarketOpen(self.syms[0], 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp: return
        w = 1.0 / len(self.syms)
        for sym in self.syms:
            self.SetHoldings(sym, w)

    def OnData(self, data): pass
