from AlgorithmImports import *
class CC18_044(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=14; self._ps=7; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _eom(self,sym,p):
        h=self.History(sym,p+2,Resolution.Daily)
        if h.empty or len(h)<p+1: return None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        vo=[float(x) for x in h["volume"].values]
        raw=[]
        for i in range(1,len(hi)):
            mid=(hi[i]+lo[i])/2-(hi[i-1]+lo[i-1])/2
            rng=hi[i]-lo[i]
            if rng==0 or vo[i]==0: continue
            raw.append(mid/(vo[i]/rng))
        if len(raw)<p: return None
        return sum(raw[-p:])/p
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            slow=self._eom(self.syms[t],self._p)
            fast=self._eom(self.syms[t],self._ps)
            if slow is not None and fast is not None and slow>0 and fast>0:
                bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
