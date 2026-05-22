from AlgorithmImports import *


class Algo058(QCAlgorithm):
    """#058 — QQQ SMA(200) trend + stretch filter: enter if stretch < 15%, exit if stretch > 20% or below SMA."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
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

        price   = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        stretch = (price - sma_val) / sma_val if sma_val > 0 else 0

        if not self.Portfolio[self.tqqq].Invested:
            if price > sma_val and stretch < 0.15:
                self.SetHoldings(self.tqqq, 1.0)
                self.Liquidate(self.bil)
        else:
            if price < sma_val or stretch > 0.20:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
