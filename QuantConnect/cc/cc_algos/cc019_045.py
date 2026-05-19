from AlgorithmImports import *
import math
class CC19_045(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.sp=5; self.lp=20; self.thr=1.2
        self.closes=RollingWindow[float](self.lp+2)
        self.syms=[]; self.st=None; self.SetWarmUp(self.lp+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def _hv(self,p):
        if not self.closes.IsReady: return None
        rets=[math.log(self.closes[i]/self.closes[i+1]) for i in range(p) if self.closes[i+1]>0]
        if len(rets)<2: return None
        m=sum(rets)/len(rets); v=sum((r-m)**2 for r in rets)/(len(rets)-1)
        return math.sqrt(v*252)
    def R(self):
        if self.IsWarmingUp or not self.closes.IsReady or not self.syms: return
        hvs=self._hv(self.sp); hvl=self._hv(self.lp)
        if hvs is None or hvl is None or hvl==0: return
        s=1 if hvs/hvl<self.thr else 0
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
        if d.Bars.ContainsKey(self.q): self.closes.Add(d.Bars[self.q].Close)
