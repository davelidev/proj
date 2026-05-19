from AlgorithmImports import *
class CC18_027(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._lo=30; self._sh=22; self._sm=20; self.SetWarmUp(60,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _coppock(self,sym):
        n=self._lo+self._sm+2
        h=self.History(sym,n,Resolution.Daily)
        if h.empty or len(h)<n: return None
        c=[float(x) for x in h["close"].values]
        roc_vals=[]
        for i in range(self._sm):
            idx=len(c)-self._sm+i
            if c[idx-self._lo]!=0 and c[idx-self._sh]!=0:
                roc_vals.append((c[idx]-c[idx-self._lo])/c[idx-self._lo]*100+(c[idx]-c[idx-self._sh])/c[idx-self._sh]*100)
            else: roc_vals.append(0)
        w=list(range(1,self._sm+1)); denom=sum(w)
        return sum(w[i]*roc_vals[i] for i in range(self._sm))/denom
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._coppock(self.syms[t])
            if v is not None and v>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
