from AlgorithmImports import *


class Algo029(QCAlgorithm):
    """50/50 TQQQ + UPRO with monthly rebalance — vol harvesting pair."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.upro = self.AddEquity("UPRO", Resolution.Daily).Symbol

        self.SetWarmUp(5, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart(self.tqqq),
            self.TimeRules.AfterMarketOpen(self.tqqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        self.SetHoldings(self.tqqq, 0.50)
        self.SetHoldings(self.upro, 0.50)
