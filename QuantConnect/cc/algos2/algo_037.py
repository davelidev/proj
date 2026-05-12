from AlgorithmImports import *


class Algo037(QCAlgorithm):
    """#37 — TQQQ "Sell in May": hold Nov-Apr, flat May-Oct."""

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
        m = self.Time.month
        in_season = m in (11, 12, 1, 2, 3, 4)
        invested = self.Portfolio[self.tqqq].Invested
        if in_season and not invested:
            self.SetHoldings(self.tqqq, 1.0)
        elif not in_season and invested:
            self.Liquidate(self.tqqq)
