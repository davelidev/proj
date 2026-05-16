from AlgorithmImports import *

class FourState_ROC10_ROC40_D200(QCAlgorithm):
    """4-state: filters = ROC(10) > 0, ROC(40) > 0, QQQ > Donchian-200 midline."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc10 = self.ROC(self.qqq, 10, Resolution.Daily)
        self.roc40 = self.ROC(self.qqq, 40, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc10.IsReady and self.roc40.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        n = int(self.roc10.Current.Value > 0) + int(self.roc40.Current.Value > 0) + int(price > mid)
        sizes = {3: (1.0, 0.0), 2: (0.7, 0.3), 1: (0.3, 0.7), 0: (0.0, 1.0)}
        wt, wb = sizes[n]
        if n != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = n

    def OnData(self, data): pass
