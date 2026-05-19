from AlgorithmImports import *
class CC18_005(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._psar=self.PSAR(self.q,0.02,0.02,0.2,Resolution.Daily)
        self.symbols=[]; self._st=None; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,coarse):
        return [x.Symbol for x in sorted(coarse,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,fine):
        self.symbols=[x.Symbol for x in sorted(fine,key=lambda x:x.MarketCap,reverse=True)[:5]]
        return self.symbols
    def R(self):
        if self.IsWarmingUp or not self._psar.IsReady or not self.symbols: return
        price=self.Securities[self.q].Price
        st=1 if price>self._psar.Current.Value else 0
        if st==self._st: return
        self._st=st
        if st==1:
            self.SetHoldings(self.b,0)
            per=1.0/len(self.symbols)
            for s in self.symbols: self.SetHoldings(s,per)
        else:
            for s in self.symbols: self.SetHoldings(s,0)
            self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
