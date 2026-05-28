from AlgorithmImports import *
class CC20_011(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.aroon=self.AROON(self.q,25,Resolution.Daily)
        self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self.aroon.IsReady: return
        bull=self.aroon.Current.Value>0
        self.SetHoldings(self.t,1.0 if bull else 0)
        self.SetHoldings(self.b,0 if bull else 1.0)
    def OnData(self,d): pass
