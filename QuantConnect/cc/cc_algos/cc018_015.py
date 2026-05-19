from AlgorithmImports import *
class CC18_015(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=15; self._st=None; self.SetWarmUp(60,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("QQQ"),self.TimeRules.AfterMarketOpen("QQQ",30),self.R)
    def _trix(self,sym,p):
        n=p*3+5
        h=self.History(sym,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        k=2.0/(p+1)
        e1=[c[0]]
        for v in c[1:]: e1.append(v*k+e1[-1]*(1-k))
        e2=[e1[0]]
        for v in e1[1:]: e2.append(v*k+e2[-1]*(1-k))
        e3=[e2[0]]
        for v in e2[1:]: e3.append(v*k+e3[-1]*(1-k))
        if len(e3)<2 or e3[-2]==0: return None
        return (e3[-1]-e3[-2])/e3[-2]*100
    def R(self):
        if self.IsWarmingUp: return
        v=self._trix(self.q,self._p)
        if v is None: return
        st=1 if v>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
