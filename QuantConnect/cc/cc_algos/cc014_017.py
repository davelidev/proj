from AlgorithmImports import *
class CC14_OBV5_Bin(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(80,Resolution.Daily); self.symbols=[]; self._st=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def CoarseSelection(self,c): return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f): self.symbols=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.symbols
    def _set(self,wt,wm,wc):
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq,self.tqqq,self.bil) or sym in self.symbols: continue
            if self.Portfolio[sym].Invested: self.Liquidate(sym)
        self.SetHoldings(self.tqqq,wt); per=wm/len(self.symbols) if wm>0 else 0
        for s in self.symbols: self.SetHoldings(s,per)
        self.SetHoldings(self.bil,wc)
    def _obv_up(self,n):
        h=self.History(self.qqq,n+5,Resolution.Daily)
        if h.empty or len(h)<n+2: return None
        c=[float(x) for x in h['close'].values]; v=[float(x) for x in h['volume'].values]
        obv=[0.0]
        for i in range(1,len(c)): obv.append(obv[-1]+(v[i] if c[i]>c[i-1] else -v[i] if c[i]<c[i-1] else 0.0))
        return obv[-1]>obv[-n-1]
    def Rebalance(self):
        if self.IsWarmingUp or not self.symbols: return
        up=self._obv_up(5)
        if up is None: return
        st=2 if up else 0
        if st==self._st: return
        self._st=st; self._set(*({2:(1,0,0),0:(0,0,1)}[st]))
    def OnData(self,data): pass
