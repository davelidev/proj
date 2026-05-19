from AlgorithmImports import *
class CC18_034(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(60,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _fi_ema(self,sym,p):
        h=self.History(sym,p+2,Resolution.Daily)
        if h.empty or len(h)<p+1: return None
        c=[float(x) for x in h["close"].values]
        v=[float(x) for x in h["volume"].values]
        fi=[(c[i]-c[i-1])*v[i] for i in range(1,len(c))]
        k=2.0/(p+1); ema=fi[0]
        for val in fi[1:]: ema=val*k+ema*(1-k)
        return ema
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            f13=self._fi_ema(self.syms[t],13); f50=self._fi_ema(self.syms[t],50)
            if f13 is not None and f50 is not None and f13>0 and f50>0:
                bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
