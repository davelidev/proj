from AlgorithmImports import *
class CC18_047(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=21; self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _vortex(self,sym):
        h=self.History(sym,self._p+2,Resolution.Daily)
        if h.empty or len(h)<self._p+1: return None,None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        cl=[float(x) for x in h["close"].values]
        vmp=sum(abs(hi[i]-lo[i-1]) for i in range(1,self._p+1))
        vmn=sum(abs(lo[i]-hi[i-1]) for i in range(1,self._p+1))
        tr=sum(max(hi[i]-lo[i],abs(hi[i]-cl[i-1]),abs(lo[i]-cl[i-1])) for i in range(1,self._p+1))
        if tr==0: return None,None
        return vmp/tr,vmn/tr
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            vp,vn=self._vortex(self.syms[t])
            if vp is not None and vp>vn: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
