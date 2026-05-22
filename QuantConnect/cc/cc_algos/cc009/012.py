from AlgorithmImports import *

class TripleMom_5state(QCAlgorithm):
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
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m10 = c[-1] > c[-11]; m30 = c[-1] > c[-31]; m90 = c[-1] > c[-91]
        n = int(in_trend)+int(m10)+int(m30)+int(m90)
        plan={4:(1.0,0.0),3:(0.75,0.25),2:(0.5,0.5),1:(0.25,0.75),0:(0.0,1.0)}
        wt,wb=plan[n]
        if n!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=n

    def OnData(self, data): pass
