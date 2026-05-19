from AlgorithmImports import *
class CC18_055(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._ema={t:self.EMA(self.syms[t],50,Resolution.Daily) for t in self.tix}
        self.SetWarmUp(65,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _uo(self,sym):
        h=self.History(sym,30,Resolution.Daily)
        if h.empty or len(h)<29: return None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        cl=[float(x) for x in h["close"].values]
        bp=[cl[i]-min(lo[i],cl[i-1]) for i in range(1,len(cl))]
        tr=[max(hi[i],cl[i-1])-min(lo[i],cl[i-1]) for i in range(1,len(cl))]
        def avg(n): s=sum(bp[-n:]); t=sum(tr[-n:]); return s/t if t else 0
        return 100*(4*avg(7)+2*avg(14)+avg(28))/(4+2+1)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            if not self._ema[t].IsReady: continue
            v=self._uo(self.syms[t])
            price=self.Securities[self.syms[t]].Price
            if v is not None and v>50 and price>self._ema[t].Current.Value:
                bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
