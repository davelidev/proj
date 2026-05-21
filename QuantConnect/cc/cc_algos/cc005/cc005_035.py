from AlgorithmImports import *

class FourState_ROC20_D100_D300(QCAlgorithm):
    """4-state with ROC(20) + Donchian-100 + Donchian-300 (longer slow filter)."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.roc   = self.ROC(self.qqq, 20, Resolution.Daily)
        self.hi100 = self.MAX(self.qqq, 100, Resolution.Daily)
        self.lo100 = self.MIN(self.qqq, 100, Resolution.Daily)
        self.hi300 = self.MAX(self.qqq, 300, Resolution.Daily)
        self.lo300 = self.MIN(self.qqq, 300, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(320, Resolution.Daily)
        self.state = None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.roc.IsReady and self.hi100.IsReady and self.lo100.IsReady
                                    and self.hi300.IsReady and self.lo300.IsReady):
            return
        mid100 = (self.hi100.Current.Value + self.lo100.Current.Value) / 2.0
        mid300 = (self.hi300.Current.Value + self.lo300.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        n = int(self.roc.Current.Value > 0) + int(price > mid100) + int(price > mid300)
        sizes = {3: (1.0, 0.0), 2: (0.7, 0.3), 1: (0.3, 0.7), 0: (0.0, 1.0)}
        wt, wb = sizes[n]
        if n != self.state:
            self.SetHoldings(self.tqqq, wt)
            self.SetHoldings(self.bil, wb)
            self.state = n

    def OnData(self, data): pass
