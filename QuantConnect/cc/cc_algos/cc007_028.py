from AlgorithmImports import *

class DownsideDeviation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]
        r=[c[i]/c[i-1]-1.0 for i in range(-20,0)]
        downs=[x for x in r if x<0]
        if not downs: dd=0
        else: dd=(sum(x**2 for x in downs)/len(downs))**0.5
        med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        calm = dd < 0.012  # downside dev < 1.2%
        if in_trend and calm: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or calm: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
