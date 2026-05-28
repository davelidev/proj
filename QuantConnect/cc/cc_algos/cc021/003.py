from AlgorithmImports import *
class CC21_086(QCAlgorithm):
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
        rets=[closes[i]/closes[i-1]-1 for i in range(1,len(closes)) if closes[i-1]>0]
        if not rets: return
        avg=sum(rets)/len(rets)
        bull=avg>0.0
        self.SetHoldings(self.t,1.0 if bull else 0)
        self.SetHoldings(self.b,0 if bull else 1.0)
    def OnData(self,d): pass
