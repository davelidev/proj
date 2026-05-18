from AlgorithmImports import *
class CC16_655(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=20; self._st=None; self._syms=[]
        self.SetWarmUp(25,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def CoarseSelection(self,coarse):
        return [x.Symbol for x in sorted(coarse,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,fine):
        self._syms=[x.Symbol for x in sorted(fine,key=lambda x:x.MarketCap,reverse=True)[:5]]
        return self._syms
    def Rebalance(self):
        if self.IsWarmingUp or not self._syms: return
        h=self.History(self.qqq,self._n+1,Resolution.Daily)
        if h.empty or len(h)<self._n: return
        upper=float(h['high'].max()); lower=float(h['low'].min())
        mid=(upper+lower)/2
        p=self.Securities[self.qqq].Price
        st=1 if p>mid else 0
        if st==self._st: return
        self._st=st
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq,self.bil) or sym in self._syms: continue
            if self.Portfolio[sym].Invested: self.Liquidate(sym)
        if st==1:
            self.SetHoldings(self.bil,0)
            per=1.0/len(self._syms)
            for s in self._syms: self.SetHoldings(s,per)
        else:
            for s in self._syms:
                if self.Portfolio[s].Invested: self.SetHoldings(s,0)
            self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
