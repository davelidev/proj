from AlgorithmImports import *
class CC18_089(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=20; self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _dc(self,sym):
        h=self.History(sym,self._p+6,Resolution.Daily)
        if h.empty or len(h)<self._p+5: return None,None
        hi=[float(x) for x in h["high"].values]
        lo=[float(x) for x in h["low"].values]
        cur_mid=(max(hi[-self._p:])+min(lo[-self._p:]))/2
        prev_mid=(max(hi[-self._p-5:-5])+min(lo[-self._p-5:-5]))/2
        return cur_mid,cur_mid>prev_mid
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            mid,rising=self._dc(self.syms[t])
            price=self.Securities[self.syms[t]].Price
            if mid is not None and price>mid and rising: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
