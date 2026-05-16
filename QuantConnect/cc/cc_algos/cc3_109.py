from AlgorithmImports import *

class TripleAND_RocAroonD200(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.roc=self.ROC(self.qqq,20,Resolution.Daily)
        self.ar=self.AROON(self.qqq,25,Resolution.Daily)
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.roc.IsReady and self.ar.IsReady and self.hi200.IsReady and self.lo200.IsReady): return
        up=self.ar.AroonUp.Current.Value; dn=self.ar.AroonDown.Current.Value
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        bull=self.roc.Current.Value>0 and (up>70 and up>dn) and self.Securities[self.qqq].Price>mid
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
