from AlgorithmImports import *

class Donchian2010Breakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.high20 = self.MAX(self.qqq, 20, Resolution.Daily)
        self.low10  = self.MIN(self.qqq, 10, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(30, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high20.IsReady and self.low10.IsReady):
            return
        price  = self.Securities[self.qqq].Price
        hi, lo = self.high20.Current.Value, self.low10.Current.Value

        if price >= hi:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif price <= lo:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
