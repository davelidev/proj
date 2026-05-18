from AlgorithmImports import *
class CC17_046(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=10; self._thresh=0.0; self._st=None
        self.SetWarmUp(15,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        import math
        h=self.History(self.q,self._n,Resolution.Daily)
        if h.empty or len(h)<self._n: return
        hi=float(h['high'].max()); lo=float(h['low'].min())
        cl=float(h['close'].iloc[-1])
        rng=hi-lo if hi!=lo else 1e-10
        val=2*((cl-lo)/rng-0.5)
        val=max(-0.999,min(0.999,val))
        fisher=0.5*math.log((1+val)/(1-val))
        st=1 if fisher>self._thresh else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
