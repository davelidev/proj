from AlgorithmImports import *

class Donchian200WithDrawdownStop(QCAlgorithm):
    """Donchian-200 midline trend with a 15%-from-20d-high drawdown emergency exit."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.high200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.low200  = self.MIN(self.qqq, 200, Resolution.Daily)
        self.high20  = self.MAX(self.qqq, 20,  Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high200.IsReady and self.low200.IsReady and self.high20.IsReady):
            return
        midline = (self.high200.Current.Value + self.low200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        dd_from_20d_high = price / self.high20.Current.Value - 1.0

        if price > midline and dd_from_20d_high > -0.15:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
