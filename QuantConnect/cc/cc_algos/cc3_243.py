from AlgorithmImports import *

class TOM_Median3State(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(220, Resolution.Daily)
        self.in_window = False; self.state=None
        self.Schedule.On(self.DateRules.MonthEnd(self.qqq, 2),
                         self.TimeRules.AfterMarketOpen(self.qqq,30), self.WindowOpen)
        self.Schedule.On(self.DateRules.MonthStart(self.qqq, 4),
                         self.TimeRules.AfterMarketOpen(self.qqq,30), self.WindowClose)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), self.Rebalance)

    def WindowOpen(self): self.in_window=True
    def WindowClose(self): self.in_window=False

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        if in_trend and self.in_window: ns,wt,wb="BULL",1.0,0.0
        elif in_trend: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
