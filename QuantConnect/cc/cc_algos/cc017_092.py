from AlgorithmImports import *
class CC17_092(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._fast=5; self._slow=34; self._thresh=0.5; self._st=None
        self.SetWarmUp(39,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        h=self.History(self.q,self._slow+1,Resolution.Daily)
        if h.empty or len(h)<self._slow: return
        import numpy as np
        mid=(h['high'].values+h['low'].values)/2
        ao=np.mean(mid[-self._fast:])-np.mean(mid[-self._slow:])
        st=1 if ao>self._thresh else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
