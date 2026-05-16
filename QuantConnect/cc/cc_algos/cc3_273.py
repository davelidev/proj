from AlgorithmImports import *

class QQQvsSHY_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.shy=self.AddEquity("SHY",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq, 200, Resolution.Daily); hs=self.History(self.shy, 60, Resolution.Daily)
        if hq.empty or hs.empty or len(hq)<200 or len(hs)<60: return
        c=[float(x) for x in hq["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        s_r=float(hs["close"].iloc[-1])/float(hs["close"].iloc[0])-1.0
        rate_calm = s_r > -0.005  # rates not spiking
        if in_trend and rate_calm: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or rate_calm: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
