from AlgorithmImports import *

class FourState_TripleROC_D200(QCAlgorithm):
    """4-state: filters = ROC(10), ROC(30), ROC(60) — 100% TQQQ if all 3 + QQQ>D200 bull."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc10 = self.ROC(self.qqq, 10, Resolution.Daily)
        self.roc30 = self.ROC(self.qqq, 30, Resolution.Daily)
        self.roc60 = self.ROC(self.qqq, 60, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc10.IsReady and self.roc30.IsReady and self.roc60.IsReady
                                    and self.hi200.IsReady and self.lo200.IsReady):
            return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        d = price > mid
        roc_count = int(self.roc10.Current.Value > 0) + int(self.roc30.Current.Value > 0) + int(self.roc60.Current.Value > 0)

        if roc_count == 3 and d: ns, wt, wb = 3, 1.0, 0.0
        elif roc_count >= 2 and d: ns, wt, wb = 2, 0.7, 0.3
        elif roc_count >= 1 and d: ns, wt, wb = 1, 0.3, 0.7
        else: ns, wt, wb = 0, 0.0, 1.0

        if ns != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = ns

    def OnData(self, data): pass
