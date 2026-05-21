from AlgorithmImports import *

class VolContractionRegime(QCAlgorithm):
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
        c=[float(x) for x in h["close"].values]
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        s=r[-10:]; l=r[-60:]
        sm=sum(s)/10; lm=sum(l)/60
        sv=(sum((x-sm)**2 for x in s)/10)**0.5
        lv=(sum((x-lm)**2 for x in l)/60)**0.5
        med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        # bull: vol contracted (sv < lv)
        vol_quiet = sv < lv
        if in_trend and vol_quiet: ns,wt,wb="BULL",1.0,0.0
        elif in_trend or vol_quiet: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
