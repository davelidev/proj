from AlgorithmImports import *

class VarianceRatio(QCAlgorithm):
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
        c=[float(x) for x in h["close"].values]
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        # var(r) and var of k-day returns
        m=sum(r)/len(r)
        var1=sum((x-m)**2 for x in r)/len(r)
        # 5-day returns
        r5=[c[i]/c[i-5]-1.0 for i in range(5,len(c))]
        m5=sum(r5)/len(r5)
        var5=sum((x-m5)**2 for x in r5)/len(r5)
        if var1<=0: return
        vr=var5/(5*var1)
        h2=self.History(self.qqq, 200, Resolution.Daily)
        if h2.empty or len(h2)<200: return
        med=sorted(float(x) for x in h2["close"].values)[100]
        in_trend=self.Securities[self.qqq].Price>med
        v_bull = vr > 1.0  # trending
        if in_trend and v_bull: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or v_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
