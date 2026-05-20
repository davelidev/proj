from AlgorithmImports import *

class TS_R20_D225_70_30(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.roc=self.ROC(self.qqq,20,Resolution.Daily)
        self.hi=self.MAX(self.qqq,225,Resolution.Daily); self.lo=self.MIN(self.qqq,225,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(245, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not(self.roc.IsReady and self.hi.IsReady and self.lo.IsReady): return
        mid=(self.hi.Current.Value+self.lo.Current.Value)/2.0
        m=self.roc.Current.Value>0; d=self.Securities[self.qqq].Price>mid
        if m and d: ns,wt,wb="BULL",1.0,0.0
        elif m or d: ns,wt,wb="MIXED",0.7,0.3
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
