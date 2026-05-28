from AlgorithmImports import *
class CC20_074(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(25,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        h=self.History(self.q,20+1,Resolution.Daily)
        if len(h)<20+1: return
        closes=list(h['close'])
        changes=[closes[i]-closes[i-1] for i in range(1,len(closes))]
        up=sum(c for c in changes if c>0); dn=sum(-c for c in changes if c<0)
        tot=up+dn
        if tot==0: return
        cmo=100*(up-dn)/tot
        bull=cmo>0
        self.SetHoldings(self.t,1.0 if bull else 0)
        self.SetHoldings(self.b,0 if bull else 1.0)
    def OnData(self,d): pass
