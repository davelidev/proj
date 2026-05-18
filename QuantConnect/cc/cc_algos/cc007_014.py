from AlgorithmImports import *

class HurstExponent(QCAlgorithm):
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
        import math
        h=self.History(self.qqq, 100, Resolution.Daily)
        if h.empty or len(h)<100: return
        c=[float(x) for x in h["close"].values]
        # Simplified Hurst: regress log(R/S) on log(n)
        lrs=[]
        for n in [10, 20, 40, 80]:
            if len(c) < n: continue
            sample=c[-n:]
            r=[sample[i]/sample[i-1]-1.0 for i in range(1,len(sample))]
            m=sum(r)/len(r)
            cum=[]; s=0
            for x in r: s+=(x-m); cum.append(s)
            R=max(cum)-min(cum)
            sd=(sum((x-m)**2 for x in r)/len(r))**0.5
            if sd<=0 or R<=0: continue
            lrs.append((math.log(n), math.log(R/sd)))
        if len(lrs)<2: return
        xs=[a for a,b in lrs]; ys=[b for a,b in lrs]
        mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(len(xs)))
        den=sum((xs[i]-mx)**2 for i in range(len(xs)))
        if den<=0: return
        H=num/den
        h2=self.History(self.qqq, 200, Resolution.Daily)
        if h2.empty or len(h2)<200: return
        med=sorted(float(x) for x in h2["close"].values)[100]
        in_trend=self.Securities[self.qqq].Price>med
        h_bull = H > 0.55
        if in_trend and h_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or h_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
