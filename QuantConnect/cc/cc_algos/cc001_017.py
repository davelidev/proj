from AlgorithmImports import *

class ThreeState_DualROC(QCAlgorithm):
    """3-state with ROC(20) > 0 AND ROC(60) > 0 consensus + Donchian-200 mid."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc20 = self.ROC(self.qqq, 20, Resolution.Daily)
        self.roc60 = self.ROC(self.qqq, 60, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc20.IsReady and self.roc60.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        m = self.roc20.Current.Value > 0 and self.roc60.Current.Value > 0
        d = price > mid
        if m and d: ns, wt, wb = "BULL", 1.0, 0.0
        elif m or d: ns, wt, wb = "MIXED", 0.5, 0.5
        else: ns, wt, wb = "BEAR", 0.0, 1.0
        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
