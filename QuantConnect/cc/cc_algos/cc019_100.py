from AlgorithmImports import *
class CC19_100(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._atr=self.ATR(self.q,14,Resolution.Daily)
        self.km=2.5
        self.sup=None; self.slo=None; self.trend=0; self.pc=None
        self.syms=[]; self.st=None; self.SetWarmUp(14+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def R(self):
        if self.IsWarmingUp or not self._atr.IsReady or not self.syms: return
        s=1 if self.trend==1 else 0
        if s==self.st: return
        self.st=s
        if s:
            self.SetHoldings(self.b,0)
            w=1.0/len(self.syms)
            for sym in self.syms: self.SetHoldings(sym,w)
        else:
            for sym in self.syms: self.SetHoldings(sym,0)
            self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if not d.Bars.ContainsKey(self.q) or not self._atr.IsReady: return
        bar=d.Bars[self.q]; atr=self._atr.Current.Value
        hl2=(bar.High+bar.Low)/2
        bu=hl2+self.km*atr; bl=hl2-self.km*atr
        if self.sup is None:
            self.sup=bu; self.slo=bl; self.trend=1
        else:
            pc=self.pc if self.pc else bar.Close
            nsu=bu if bu<self.sup or pc>self.sup else self.sup
            nsl=bl if bl>self.slo or pc<self.slo else self.slo
            if self.trend==1:
                self.trend=1 if bar.Close>=nsl else -1
            else:
                self.trend=-1 if bar.Close<=nsu else 1
            self.sup=nsu; self.slo=nsl
        self.pc=bar.Close
