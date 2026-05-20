from AlgorithmImports import *

class RangeCompressed_T12(QCAlgorithm):
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
        # Sum of high-low ranges over last 25 / avg range over 200
        recent_r=[float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(-25,0)]
        all_r=[float(h["high"].iloc[i])-float(h["low"].iloc[i]) for i in range(-200,0)]
        avg_recent=sum(recent_r)/25
        avg_all=sum(all_r)/200
        compressed = avg_recent < avg_all * 1.2
        if in_trend and compressed: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or compressed: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
