from AlgorithmImports import *
class CC17_044(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._ws=6; self._wm=12; self._wl=24; self._thresh=50
        self._st=None; self.SetWarmUp(29,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        import numpy as np
        n=self._wl+1
        h=self.History(self.q,n,Resolution.Daily)
        if h.empty or len(h)<n: return
        hi=h['high'].values; lo=h['low'].values; cl=h['close'].values
        pc=np.roll(cl,1); pc[0]=cl[0]
        bp=cl-np.minimum(lo,pc); tr=np.maximum(hi,pc)-np.minimum(lo,pc)
        tr=np.where(tr==0,1e-10,tr)
        def avg(p): return np.sum(bp[-p:])/max(np.sum(tr[-p:]),1e-10)
        uo=100*(4*avg(self._ws)+2*avg(self._wm)+avg(self._wl))/7
        st=1 if uo>self._thresh else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
