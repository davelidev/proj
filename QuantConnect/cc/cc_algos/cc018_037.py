from AlgorithmImports import *
class CC18_037(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._r=13; self._s=7; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _tsi(self,sym):
        need=self._r+self._s+5
        h=self.History(sym,need+2,Resolution.Daily)
        if h.empty or len(h)<need: return None
        c=[float(x) for x in h["close"].values]
        pc=[c[i]-c[i-1] for i in range(1,len(c))]
        apc=[abs(x) for x in pc]
        k1=2.0/(self._r+1)
        e1p=[pc[0]]
        for v in pc[1:]: e1p.append(v*k1+e1p[-1]*(1-k1))
        e1a=[apc[0]]
        for v in apc[1:]: e1a.append(v*k1+e1a[-1]*(1-k1))
        k2=2.0/(self._s+1)
        e2p=[e1p[0]]
        for v in e1p[1:]: e2p.append(v*k2+e2p[-1]*(1-k2))
        e2a=[e1a[0]]
        for v in e1a[1:]: e2a.append(v*k2+e2a[-1]*(1-k2))
        if e2a[-1]==0: return None
        return 100*e2p[-1]/e2a[-1]
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._tsi(self.syms[t])
            if v is not None and v>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
