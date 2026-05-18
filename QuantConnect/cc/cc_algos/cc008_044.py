from AlgorithmImports import *

class Mom252_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(280, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 252, Resolution.Daily)
        if h.empty or len(h)<252: return
        c=[float(x) for x in h["close"].values]
        # 200-day median
        med=sorted(c[-200:])[100]
        in_trend = self.Securities[self.qqq].Price > med
        ann_ret = c[-1]/c[0] - 1.0
        ann_bull = ann_ret > 0
        if in_trend and ann_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or ann_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
