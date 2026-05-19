from AlgorithmImports import *
class CC18_054(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _uo(self,sym,s,m,l):
        need=l+2
        h=self.History(sym,need,Resolution.Daily)
        if h.empty or len(h)<need-1: return None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        cl=[float(x) for x in h["close"].values]
        bp=[cl[i]-min(lo[i],cl[i-1]) for i in range(1,len(cl))]
        tr=[max(hi[i],cl[i-1])-min(lo[i],cl[i-1]) for i in range(1,len(cl))]
        def avg(n): sv=sum(bp[-n:]); t=sum(tr[-n:]); return sv/t if t else 0
        return 100*(4*avg(s)+2*avg(m)+avg(l))/(4+2+1)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            v=self._uo(self.syms[t],5,10,20)
            if v is not None and v>50: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
