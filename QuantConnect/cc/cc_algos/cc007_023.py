from AlgorithmImports import *

class OBVSlopeHist(QCAlgorithm):
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
        c=[float(x) for x in h["close"].values]; v=[float(x) for x in h["volume"].values]
        obv=0.0; obvs=[]
        for i in range(1,len(c)):
            sign = 1 if c[i]>c[i-1] else (-1 if c[i]<c[i-1] else 0)
            obv += sign*v[i]; obvs.append(obv)
        ys=obvs[-30:]; n=30
        xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
        den=sum((xs[i]-mx)**2 for i in range(n))
        if den<=0: return
        slope=num/den
        med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        ob_bull = slope > 0
        if in_trend and ob_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or ob_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
