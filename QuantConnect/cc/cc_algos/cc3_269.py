from AlgorithmImports import *

class AboveCloud(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.h9=self.MAX(self.qqq, 9, Resolution.Daily); self.l9=self.MIN(self.qqq, 9, Resolution.Daily)
        self.h26=self.MAX(self.qqq, 26, Resolution.Daily); self.l26=self.MIN(self.qqq, 26, Resolution.Daily)
        self.h52=self.MAX(self.qqq, 52, Resolution.Daily); self.l52=self.MIN(self.qqq, 52, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not (self.h9.IsReady and self.l9.IsReady and self.h26.IsReady and self.l26.IsReady and self.h52.IsReady and self.l52.IsReady): return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        sa=((self.h9.Current.Value+self.l9.Current.Value)/2.0 + (self.h26.Current.Value+self.l26.Current.Value)/2.0)/2.0
        sb=(self.h52.Current.Value+self.l52.Current.Value)/2.0
        cloud_top=max(sa,sb); cloud_bot=min(sa,sb)
        price=self.Securities[self.qqq].Price
        above_cloud = price > cloud_top
        if in_trend and above_cloud: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or above_cloud: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
