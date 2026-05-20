from AlgorithmImports import *

class FourState_ROC20_Aroon25_D200(QCAlgorithm):
    """4-state with ROC(20) + Aroon-25 + Donchian-200 midline."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.aroon = self.AROON(self.qqq, 25, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.aroon.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        up = self.aroon.AroonUp.Current.Value
        dn = self.aroon.AroonDown.Current.Value
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        n = int(self.roc.Current.Value > 0) + int(up > 70 and up > dn) + int(price > mid)
        sizes = {3: (1.0, 0.0), 2: (0.7, 0.3), 1: (0.3, 0.7), 0: (0.0, 1.0)}
        wt, wb = sizes[n]
        if n != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = n

    def OnData(self, data): pass
