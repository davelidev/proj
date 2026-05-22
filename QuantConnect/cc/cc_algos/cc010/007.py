from AlgorithmImports import *

class Mom20_OBV_ADX_Med_5state(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.adx=self.ADX(self.qqq, 14, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.adx.IsReady: return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]; v=[float(x) for x in h["volume"].values]; med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        m20 = c[-1] > c[-21]
        adx_b = self.adx.PositiveDirectionalIndex.Current.Value > self.adx.NegativeDirectionalIndex.Current.Value
        obv=0.0; obvs=[]
        for i in range(1,len(c)):
            sign = 1 if c[i]>c[i-1] else (-1 if c[i]<c[i-1] else 0)
            obv += sign*v[i]; obvs.append(obv)
        nW=30; ys=obvs[-nW:]; xs=list(range(nW))
        mx=sum(xs)/nW; my=sum(ys)/nW
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(nW))
        den=sum((xs[i]-mx)**2 for i in range(nW))
        slope=num/den if den>0 else 0
        o_b = slope > 0
        n = int(in_trend)+int(m20)+int(adx_b)+int(o_b)
        plan={4:(1.0,0.0),3:(0.75,0.25),2:(0.5,0.5),1:(0.25,0.75),0:(0.0,1.0)}
        wt,wb=plan[n]
        if n!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=n

    def OnData(self, data): pass
