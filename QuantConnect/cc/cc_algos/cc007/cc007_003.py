from AlgorithmImports import *

class FS_R20_D100_D250(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol; self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.roc=self.ROC(self.qqq,20,Resolution.Daily)
        self.h1=self.MAX(self.qqq,100,Resolution.Daily); self.l1=self.MIN(self.qqq,100,Resolution.Daily)
        self.h2=self.MAX(self.qqq,250,Resolution.Daily); self.l2=self.MIN(self.qqq,250,Resolution.Daily)
        self.hi20=self.MAX(self.qqq,20,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(270, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.roc.IsReady and self.h1.IsReady and self.l1.IsReady and self.h2.IsReady and self.l2.IsReady and self.hi20.IsReady): return
        m1=(self.h1.Current.Value+self.l1.Current.Value)/2.0
        m2=(self.h2.Current.Value+self.l2.Current.Value)/2.0
        price=self.Securities[self.qqq].Price; dd_20=price/self.hi20.Current.Value-1.0
        bull=self.roc.Current.Value>0 and price>m1 and price>m2 and dd_20 > -1.0000
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
