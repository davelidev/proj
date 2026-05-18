from AlgorithmImports import *
class CC17_010(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._bb=self.BB(self.q,25,2.2,MovingAverageType.Simple,Resolution.Daily)
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._bb.IsReady: return
        p=self.Securities[self.q].Price
        upper=self._bb.UpperBand.Current.Value; lower=self._bb.LowerBand.Current.Value
        mid=self._bb.MiddleBand.Current.Value
        st=1 if p>mid else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
