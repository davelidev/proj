from AlgorithmImports import *


class Algo057(QCAlgorithm):
    """#057 — QQQ SMA(200) trend + vol ratio (STD10/STD60 < 1.2): 100% TQQQ, else BIL."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.sma       = self.SMA(self.qqq, 200, Resolution.Daily)
        self.std_short = self.STD(self.qqq,  10, Resolution.Daily)
        self.std_long  = self.STD(self.qqq,  60, Resolution.Daily)
        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not (self.sma.IsReady and self.std_short.IsReady and self.std_long.IsReady): return

        ratio = (self.std_short.Current.Value / self.std_long.Current.Value
                 if self.std_long.Current.Value > 0 else 1.0)
        bull  = self.Securities[self.qqq].Price > self.sma.Current.Value and ratio < 1.2

        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
