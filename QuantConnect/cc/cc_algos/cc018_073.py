from AlgorithmImports import *
class CC18_073(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=14; self.SetWarmUp(25,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _willr(self,sym):
        h=self.History(sym,self._p+1,Resolution.Daily)
        if h.empty or len(h)<self._p: return None
        hi=[float(x) for x in h["high"].values[-self._p:]]
        lo=[float(x) for x in h["low"].values[-self._p:]]
        cl=float(h["close"].values[-1])
        hh=max(hi); ll=min(lo)
        if hh==ll: return None
        return (hh-cl)/(hh-ll)*-100
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._willr(self.syms[t])
            if v is not None and v>-40: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
