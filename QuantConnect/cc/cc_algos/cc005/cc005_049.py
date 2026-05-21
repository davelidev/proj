from AlgorithmImports import *

class TQQQPyramid30(QCAlgorithm):
    """Pyramid: +30% TQQQ each day in trend (full in ~4 days), full exit on bear flip."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.exposure = 0.0

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        bull = self.roc.Current.Value > 0 and self.Securities[self.qqq].Price > mid
        new_exp = min(1.0, self.exposure + 0.3) if bull else 0.0
        if abs(new_exp - self.exposure) > 0.01:
            self.SetHoldings(self.tqqq, new_exp)
            self.SetHoldings(self.bil, 1.0 - new_exp)
            self.exposure = new_exp

    def OnData(self, data): pass
