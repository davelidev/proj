from AlgorithmImports import *


class Algo024(QCAlgorithm):
    """80% TQQQ + 20% VXX hedge overlay, monthly rebalance."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.vxx = self.AddEquity("VXX", Resolution.Daily).Symbol

        self.SetWarmUp(5, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.tqqq),
            self.TimeRules.AfterMarketOpen(self.tqqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        self.SetHoldings(self.tqqq, 0.80)
        self.SetHoldings(self.vxx, 0.20)
