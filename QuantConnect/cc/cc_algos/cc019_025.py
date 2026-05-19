from AlgorithmImports import *
class CC19_025(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._bb=self.BB(self.q,20,2.0,MovingAverageType.Simple,Resolution.Daily)
        self._atr=self.ATR(self.q,20,Resolution.Daily)
        self.km=2.0; self.syms=[]; self.st=None; self.SetWarmUp(max(20,20)+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def R(self):
        if self.IsWarmingUp or not self._bb.IsReady or not self._atr.IsReady or not self.syms: return
        bb_hw=(self._bb.UpperBand.Current.Value-self._bb.LowerBand.Current.Value)/2
        in_sq=bb_hw<self.km*self._atr.Current.Value
        close=self.Securities[self.q].Price
        above_mid=close>self._bb.MiddleBand.Current.Value
        s=1 if (not in_sq) and above_mid else 0
        if s==self.st: return
        self.st=s
        if s:
            self.SetHoldings(self.b,0)
            w=1.0/len(self.syms)
            for sym in self.syms: self.SetHoldings(sym,w)
        else:
            for sym in self.syms: self.SetHoldings(sym,0)
            self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
