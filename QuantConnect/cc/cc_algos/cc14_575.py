from AlgorithmImports import *
class CC14_OBV30_ADX20(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._adx=self.ADX("QQQ",20,Resolution.Daily)
        self.SetWarmUp(60,Resolution.Daily); self.symbols=[]; self._st=None
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
    def Rebalance(self):
        if self.IsWarmingUp or not self._adx.IsReady or not self.symbols: return
        h=self.History(self.qqq,30+5,Resolution.Daily)
        if h.empty or len(h)<30+2: return
        c=[float(x) for x in h['close'].values]; v=[float(x) for x in h['volume'].values]
        obv=[0.0]
        for i in range(1,len(c)): obv.append(obv[-1]+(v[i] if c[i]>c[i-1] else -v[i] if c[i]<c[i-1] else 0.0))
        obv_up=obv[-1]>obv[-30-1]
        pdi=self._adx.PositiveDirectionalIndex.Current.Value; ndi=self._adx.NegativeDirectionalIndex.Current.Value
        adx_val=self._adx.Current.Value
        adx_bull=pdi>ndi; adx_bear=adx_val>25 and ndi>pdi
        if obv_up and adx_bull: st=2
        elif (not obv_up) or adx_bear: st=0
        else: st=1
        if st==self._st: return
        self._st=st; self._set(*{2:(1,0,0),1:(0,1,0),0:(0,0,1)}[st])
    def OnData(self,data): pass
