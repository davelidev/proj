from AlgorithmImports import *

class Skewness60(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 61, Resolution.Daily)
        if h.empty or len(h)<61: return
        c=[float(x) for x in h["close"].values]
        r=[c[i]/c[i-1]-1.0 for i in range(1,len(c))]
        n=len(r); m=sum(r)/n
        v=sum((x-m)**2 for x in r)/n; sd=v**0.5
        if sd<=0: return
        skew=sum((x-m)**3 for x in r)/n/(sd**3)
        bull = skew > 0
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
