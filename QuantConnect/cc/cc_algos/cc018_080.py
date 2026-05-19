from AlgorithmImports import *
class CC18_080(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _adm(self,sym,p):
        h=self.History(sym,p+1,Resolution.Daily)
        if h.empty or len(h)<p: return None
        hi=[float(x) for x in h["high"].values[-p:]]
        lo=[float(x) for x in h["low"].values[-p:]]
        cl=[float(x) for x in h["close"].values[-p:]]
        vo=[float(x) for x in h["volume"].values[-p:]]
        adv=[((cl[i]-lo[i])-(hi[i]-cl[i]))/(hi[i]-lo[i])*vo[i] if hi[i]!=lo[i] else 0 for i in range(p)]
        return sum(adv)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            f=self._adm(self.syms[t],5); s=self._adm(self.syms[t],20)
            if f is not None and s is not None and f>0 and s>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
