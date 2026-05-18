from AlgorithmImports import *

class PercentileRank100(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily)
        self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 100, Resolution.Daily)
        if h.empty or len(h)<100: return
        c=sorted(float(x) for x in h["close"].values)
        cur=self.Securities[self.qqq].Price
        pct=sum(1 for v in c if v<=cur)/len(c)
        h2=self.History(self.qqq, 200, Resolution.Daily)
        if h2.empty or len(h2)<200: return
        med=sorted(float(x) for x in h2["close"].values)[100]
        in_trend=cur>med
        p_bull = pct > 0.7
        if in_trend and p_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or p_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
