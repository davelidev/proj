from AlgorithmImports import *

class TwoState_CMO_52wHigh(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi252=self.MAX(self.qqq,252,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(270, Resolution.Daily); self.state=None

    def Rebalance(self):
        if self.IsWarmingUp or not self.hi252.IsReady: return
        h=self.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h)<21: return
        c=[float(x) for x in h["close"].values]
        ch=[c[i]-c[i-1] for i in range(1,len(c))]
        up=sum(x for x in ch if x>0); dn=sum(-x for x in ch if x<0); tot=up+dn
        if tot<=0: return
        cmo = 100.0*(up-dn)/tot
        dd = self.Securities[self.qqq].Price/self.hi252.Current.Value-1.0
        bull = cmo > 0 and dd > -0.15
        ns = "BULL" if bull else "BEAR"
        if ns != self.state:
            self.SetHoldings(self.tqqq, 1.0 if bull else 0.0)
            self.SetHoldings(self.bil,  0.0 if bull else 1.0)
            self.state = ns

    def OnData(self, data): pass
