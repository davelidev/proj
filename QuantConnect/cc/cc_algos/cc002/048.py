from AlgorithmImports import *


class Algo055(QCAlgorithm):
    """#055 — QQQ SMA(200) trend: 100% TQQQ above, 100% BIL below."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        if self.Securities[self.qqq].Price > self.sma.Current.Value:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
