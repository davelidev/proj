from AlgorithmImports import *
class CC17_074(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=14; self._thresh=5; self.SetWarmUp(19,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            h=self.History(self.syms[t],self._n+1,Resolution.Daily)
            if h.empty or len(h)<self._n+1: continue
            cl=h['close'].values
            diffs=[cl[j]-cl[j-1] for j in range(1,len(cl))]
            up=sum(d for d in diffs if d>0); dn=sum(-d for d in diffs if d<0)
            cmo=100*(up-dn)/(up+dn+1e-10)
            if cmo>self._thresh: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
