from AlgorithmImports import *
class CC21_074(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.atr_s=self.ATR(self.q,14,MovingAverageType.Simple,Resolution.Daily)
        self.atr_l=self.ATR(self.q,60,MovingAverageType.Simple,Resolution.Daily)
        self.SetWarmUp(65,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),
                         self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self.atr_s.IsReady or not self.atr_l.IsReady: return
        price=self.Securities[self.q].Price
        if price==0: return
        bull=self.atr_s.Current.Value<self.atr_l.Current.Value
        self.SetHoldings(self.t,1.0 if bull else 0)
        self.SetHoldings(self.b,0 if bull else 1.0)
    def OnData(self,d): pass
