from AlgorithmImports import *

class ROCD100_Trail5(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.roc=self.ROC(self.qqq,20,Resolution.Daily)
        self.hi100=self.MAX(self.qqq,100,Resolution.Daily); self.lo100=self.MIN(self.qqq,100,Resolution.Daily)
        self.hi20=self.MAX(self.qqq,20,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.roc.IsReady and self.hi100.IsReady and self.lo100.IsReady and self.hi20.IsReady): return
        mid=(self.hi100.Current.Value+self.lo100.Current.Value)/2.0
        price=self.Securities[self.qqq].Price; dd=price/self.hi20.Current.Value-1.0
        bull=self.roc.Current.Value>0 and price>mid and dd>-0.05
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
