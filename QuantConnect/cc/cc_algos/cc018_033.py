from AlgorithmImports import *
class CC18_033(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=50; self.SetWarmUp(60,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _fi_ema(self,sym):
        h=self.History(sym,self._p+2,Resolution.Daily)
        if h.empty or len(h)<self._p+1: return None
        c=[float(x) for x in h["close"].values]
        v=[float(x) for x in h["volume"].values]
        fi=[(c[i]-c[i-1])*v[i] for i in range(1,len(c))]
        k=2.0/(self._p+1); ema=fi[0]
        for val in fi[1:]: ema=val*k+ema*(1-k)
        return ema
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._fi_ema(self.syms[t])
            if v is not None and v>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
