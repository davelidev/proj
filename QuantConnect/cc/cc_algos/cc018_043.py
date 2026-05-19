from AlgorithmImports import *
class CC18_043(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=21; self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _eom(self,sym):
        h=self.History(sym,self._p+2,Resolution.Daily)
        if h.empty or len(h)<self._p+1: return None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        vo=[float(x) for x in h["volume"].values]
        raw=[]
        for i in range(1,len(hi)):
            mid=(hi[i]+lo[i])/2-(hi[i-1]+lo[i-1])/2
            rng=hi[i]-lo[i]
            if rng==0 or vo[i]==0: continue
            raw.append(mid/(vo[i]/rng))
        if len(raw)<self._p: return None
        return sum(raw[-self._p:])/self._p
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._eom(self.syms[t])
            if v is not None and v>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
