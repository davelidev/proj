from AlgorithmImports import *

class HYGvsIEI_Median(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.hyg=self.AddEquity("HYG",Resolution.Daily).Symbol
        self.iei=self.AddEquity("IEI",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq, 200, Resolution.Daily)
        hh=self.History(self.hyg, 60, Resolution.Daily)
        hi=self.History(self.iei, 60, Resolution.Daily)
        if hq.empty or hh.empty or hi.empty or len(hq)<200 or len(hh)<60 or len(hi)<60: return
        c=[float(x) for x in hq["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        h_r=float(hh["close"].iloc[-1])/float(hh["close"].iloc[0])-1.0
        i_r=float(hi["close"].iloc[-1])/float(hi["close"].iloc[0])-1.0
        risk_on = h_r > i_r
        if in_trend and risk_on: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or risk_on: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
