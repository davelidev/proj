from AlgorithmImports import *
class CC14_Don20_20(QCAlgorithm):
    # Symmetric Donchian(20): enter on 20-day high, exit on 20-day low
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.SetWarmUp(40,Resolution.Daily); self.symbols=[]; self._st=None
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
        if self.IsWarmingUp or not self.symbols: return
        h=self.History(self.qqq,22,Resolution.Daily)
        if h.empty or len(h)<22: return
        hi20=float(h['high'].iloc[-20:].max())
        lo20=float(h['low'].iloc[-20:].min())
        p=self.Securities[self.qqq].Price
        if p>hi20: st=2
        elif p<lo20: st=0
        else: st=1
        if st==self._st: return
        self._st=st; self._set(*{2:(1,0,0),1:(0,1,0),0:(0,0,1)}[st])
    def OnData(self,data): pass
