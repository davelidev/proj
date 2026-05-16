from AlgorithmImports import *

class DDPlusWilliamsR(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi100=self.MAX(self.qqq, 100, Resolution.Daily)
        self.wilr=self.WILR(self.qqq, 14, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi100.IsReady and self.wilr.IsReady): return
        dd=self.Securities[self.qqq].Price/self.hi100.Current.Value-1.0
        w=self.wilr.Current.Value
        d_bull = dd > -0.07
        w_bull = w > -50
        if d_bull and w_bull: ns,wt,wb="BULL",1.0,0.0
        elif d_bull or w_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
