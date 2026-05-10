from AlgorithmImports import *


class Algo038(QCAlgorithm):
    """#38 — TQQQ overnight hold: enter at close, exit at next open ('overnight effect')."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.SetWarmUp(5, Resolution.Daily)
        # Buy near close
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.BeforeMarketClose(self.tqqq, 5),
                         self.GoLong)
        # Sell at open
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 5),
                         self.GoFlat)

    def GoLong(self):
        if self.IsWarmingUp: return
        if not self.Portfolio[self.tqqq].Invested:
            self.SetHoldings(self.tqqq, 1.0)

    def GoFlat(self):
        if self.IsWarmingUp: return
        if self.Portfolio[self.tqqq].Invested:
            self.Liquidate(self.tqqq)
