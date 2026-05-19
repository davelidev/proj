from AlgorithmImports import *
class CC19_069(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._macd=self.MACD(self.q,12,26,1,Resolution.Daily)
        self.sp=10
        self.mw=RollingWindow[float](self.sp+1)
        self.kw=RollingWindow[float](self.sp+1)
        self.thr=25.0; self.syms=[]; self.st=None; self.SetWarmUp(26+self.sp*2+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def _stoch(self,w):
        vals=[w[i] for i in range(self.sp+1)]
        hh=max(vals); ll=min(vals)
        if hh==ll: return 50.0
        return (vals[0]-ll)/(hh-ll)*100
    def R(self):
        if self.IsWarmingUp or not self._macd.IsReady or not self.syms: return
        self.mw.Add(self._macd.Current.Value)
        if not self.mw.IsReady: return
        k1=self._stoch(self.mw)
        self.kw.Add(k1)
        if not self.kw.IsReady: return
        stc=self._stoch(self.kw)
        s=1 if stc>self.thr else 0
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
