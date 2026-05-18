from AlgorithmImports import *
class CC17_083(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.tix=['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL']
        self.syms={t:self.AddEquity(t,Resolution.Daily).Symbol for t in self.tix}
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._atr={t:self.ATR(self.syms[t],10,MovingAverageType.Simple,Resolution.Daily) for t in self.tix}
        self._lb=100; self._pct=50; self._atrhist={t:[] for t in self.tix}
        self.SetWarmUp(115,Resolution.Daily)
        self.Schedule.On(self.DateRules.MonthStart("AAPL"),self.TimeRules.AfterMarketOpen("AAPL",30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        import numpy as np
        for t in self.tix:
            if self._atr[t].IsReady:
                self._atrhist[t].append(self._atr[t].Current.Value)
                if len(self._atrhist[t])>self._lb*2: self._atrhist[t]=self._atrhist[t][-self._lb*2:]
        bulls=[]
        for t in self.tix:
            hist=self._atrhist[t]
            if len(hist)<self._lb: continue
            cur=hist[-1]; ref=hist[-self._lb:]
            pct=100*sum(1 for x in ref if cur>x)/len(ref)
            if pct<self._pct: bulls.append(t)
        n=len(bulls)
        for t in self.tix: self.SetHoldings(self.syms[t],1.0/n if t in bulls else 0)
        self.SetHoldings(self.b,0 if bulls else 1.0)
    def OnData(self,d): pass
