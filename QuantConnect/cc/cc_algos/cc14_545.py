from AlgorithmImports import *
class CC14_ADX14_DILvl(QCAlgorithm):
    # Uses absolute DI level (>25) rather than just direction — different signal from 541-544
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._adx=self.ADX("QQQ",14,Resolution.Daily)
        self.SetWarmUp(50,Resolution.Daily); self.symbols=[]; self._st=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def CoarseSelection(self,coarse):
        return [x.Symbol for x in sorted(coarse,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,fine):
        self.symbols=[x.Symbol for x in sorted(fine,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.symbols
    def _set(self,wt,wm,wc):
        for sym in list(self.Securities.Keys):
            if sym in (self.qqq,self.tqqq,self.bil) or sym in self.symbols: continue
            if self.Portfolio[sym].Invested: self.Liquidate(sym)
        self.SetHoldings(self.tqqq,wt); per=wm/len(self.symbols) if wm>0 else 0
        for s in self.symbols: self.SetHoldings(s,per)
        self.SetHoldings(self.bil,wc)
    def Rebalance(self):
        if self.IsWarmingUp or not self._adx.IsReady or not self.symbols: return
        pdi=self._adx.PositiveDirectionalIndex.Current.Value
        ndi=self._adx.NegativeDirectionalIndex.Current.Value
        if pdi>25: st=2
        elif ndi>25: st=0
        else: st=1
        if st==self._st: return
        self._st=st; self._set(*{2:(1,0,0),1:(0,1,0),0:(0,0,1)}[st])
    def OnData(self,data): pass
