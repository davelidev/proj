from AlgorithmImports import *

class Donchian150Midline(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.high = self.MAX(self.qqq, 150, Resolution.Daily)
        self.low  = self.MIN(self.qqq, 150, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(170, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high.IsReady and self.low.IsReady):
            return
        mid = (self.high.Current.Value + self.low.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        if price > mid:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
