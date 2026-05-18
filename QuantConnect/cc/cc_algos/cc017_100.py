from AlgorithmImports import *
class CC17_100(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=25; self._thresh=0; self._st=None
        self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        h=self.History(self.q,self._n,Resolution.Daily)
        if h.empty or len(h)<self._n: return
        import numpy as np
        hi=h['high'].values; lo=h['low'].values; cl=h['close'].values; vol=h['volume'].values
        rng=hi-lo; rng=np.where(rng==0,1e-10,rng)
        mfm=((cl-lo)-(hi-cl))/rng
        cmf=np.sum(mfm*vol)/max(np.sum(vol),1)
        st=1 if cmf>self._thresh else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
