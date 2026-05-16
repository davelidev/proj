from AlgorithmImports import *

class RealizedVolBottom30(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(280, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 252, Resolution.Daily)
        if h.empty or len(h)<252: return
        c=[float(x) for x in h["close"].values]
        # rolling 20d std of returns, daily
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        vols=[]
        for i in range(20, len(r)):
            seg=r[i-20:i]
            m=sum(seg)/20; var=sum((x-m)**2 for x in seg)/20; vols.append(var**0.5)
        cur_vol = vols[-1]
        sv = sorted(vols)
        pct = sum(1 for v in sv if v<=cur_vol)/len(sv)
        med=sorted(c)[126]
        in_trend = self.Securities[self.qqq].Price > med
        low_vol = pct < 0.3
        if in_trend and low_vol: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or low_vol: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
