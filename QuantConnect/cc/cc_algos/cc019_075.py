from AlgorithmImports import *
class CC19_075(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.cw=RollingWindow[float](35)
        self.use_sig=True
        self.kbuf=RollingWindow[float](10)
        self.syms=[]; self.st=None; self.SetWarmUp(140,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def _kst(self):
        if not self.cw.IsReady: return None
        def roc(n): return (self.cw[0]-self.cw[n])/self.cw[n]*100 if self.cw[n]>0 else 0
        return roc(10)*1+roc(15)*2+roc(20)*3+roc(30)*4
    def R(self):
        if self.IsWarmingUp or not self.cw.IsReady or not self.syms: return
        kst=self._kst()
        if kst is None: return
        self.kbuf.Add(kst)
        if self.use_sig and self.kbuf.IsReady:
            sig=sum(self.kbuf[i] for i in range(9))/9
            s=1 if kst>sig and kst>0 else 0
        else:
            s=1 if kst>0 else 0
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
        if d.Bars.ContainsKey(self.q): self.cw.Add(d.Bars[self.q].Close)
