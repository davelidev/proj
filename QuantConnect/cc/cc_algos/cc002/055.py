from AlgorithmImports import *


class Algo056(QCAlgorithm):
    """#056 — QQQ SMA(200) trend + VIX < 30 filter: 100% TQQQ, else BIL."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.vix  = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol

        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        if not self.Securities.ContainsKey(self.vix): return

        bull = (self.Securities[self.qqq].Price > self.sma.Current.Value
                and self.Securities[self.vix].Price < 30)

        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
