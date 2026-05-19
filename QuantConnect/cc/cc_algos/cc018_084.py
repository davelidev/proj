from AlgorithmImports import *
class CC18_084(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._k=21; self._d=7; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _stoch(self,sym):
        h=self.History(sym,self._k+self._d+1,Resolution.Daily)
        if h.empty or len(h)<self._k+self._d: return None,None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        cl=[float(x) for x in h["close"].values]
        ks=[]
        for i in range(self._d):
            idx=len(cl)-self._d+i
            hh=max(hi[idx-self._k+1:idx+1]); ll=min(lo[idx-self._k+1:idx+1])
            ks.append((cl[idx]-ll)/(hh-ll)*100 if hh!=ll else 50)
        return ks[-1],sum(ks)/len(ks)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            k,d=self._stoch(self.syms[t])
            if k is not None and k>50: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
