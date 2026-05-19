from AlgorithmImports import *
class CC18_017(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL','MSFT','AMZN','NVDA','GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._p=20; self._thresh=0.3; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def _er(self,sym):
        h=self.History(sym,self._p+1,Resolution.Daily)
        if h.empty or len(h)<self._p+1: return None,None
        c=[float(x) for x in h["close"].values]
        direction=c[-1]-c[0]
        noise=sum(abs(c[i]-c[i-1]) for i in range(1,len(c)))
        if noise==0: return 0,direction
        return abs(direction)/noise,direction
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            er,d=self._er(self.syms[t])
            if er is not None and er>self._thresh and d>0: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
