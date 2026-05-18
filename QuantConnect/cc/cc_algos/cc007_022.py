from AlgorithmImports import *

class ADLineSlope(QCAlgorithm):
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
        ad=0.0; ads=[]
        for i in range(len(h)):
            hi=float(h["high"].iloc[i]); lo=float(h["low"].iloc[i]); cl=float(h["close"].iloc[i]); vl=float(h["volume"].iloc[i])
            if hi==lo: m=0
            else: m=((cl-lo)-(hi-cl))/(hi-lo)
            ad += m*vl
            ads.append(ad)
        # slope over last 30 of A/D
        ys=ads[-30:]; n=30
        xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
        den=sum((xs[i]-mx)**2 for i in range(n))
        if den<=0: return
        slope=num/den
        c=[float(x) for x in h["close"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        ad_bull = slope > 0
        if in_trend and ad_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or ad_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
