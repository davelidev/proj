from AlgorithmImports import *
class CC17_086(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=20; self._thresh=0; self.SetWarmUp(25,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bulls=[]
        for t in self.tix:
            h=self.History(self.syms[t],self._n,Resolution.Daily)
            if h.empty or len(h)<self._n: continue
            import numpy as np
            hi=h['high'].values; lo=h['low'].values; cl=h['close'].values; vol=h['volume'].values
            tp=(hi+lo+cl)/3
            vwap=np.sum(tp*vol)/max(np.sum(vol),1)
            cur=cl[-1]
            if cur>vwap*(1+self._thresh): bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
