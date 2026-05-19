from AlgorithmImports import *
class CC18_008(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=100; self._st=None; self.SetWarmUp(110,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def _slope(self,n):
        h=self.History(self.q,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        xm=(n-1)/2; ym=sum(c)/n
        num=sum((i-xm)*(c[i]-ym) for i in range(n))
        den=sum((i-xm)**2 for i in range(n))
        return num/den if den else 0
    def R(self):
        if self.IsWarmingUp: return
        s=self._slope(self._n)
        if s is None: return
        st=1 if s>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
