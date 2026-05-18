from AlgorithmImports import *

class TripleMFI_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.m7=self.MFI(self.qqq, 7, Resolution.Daily)
        self.m14=self.MFI(self.qqq, 14, Resolution.Daily)
        self.m30=self.MFI(self.qqq, 30, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.m7.IsReady and self.m14.IsReady and self.m30.IsReady): return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        n=int(self.m7.Current.Value>50)+int(self.m14.Current.Value>50)+int(self.m30.Current.Value>50)
        if in_trend and n==3: ns,wt,wb="BULL",1.0,0.0
        elif in_trend and n>=1: ns,wt,wb="MIXED",0.6,0.4
        elif in_trend or n>=2: ns,wt,wb="MIXED2",0.3,0.7
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
