from AlgorithmImports import *
class CC19_014(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.P=25; self.thr=26.5
        self.k=2.0/10; self.e1=None; self.e2=None
        self.mbuf=RollingWindow[float](self.P+1)
        self.syms=[]; self.st=None; self.SetWarmUp(self.P+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def R(self):
        if self.IsWarmingUp or not self.mbuf.IsReady or not self.syms: return
        mi=sum(self.mbuf[i] for i in range(self.P))
        s=1 if mi<self.thr else 0
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
        if not d.Bars.ContainsKey(self.q): return
        bar=d.Bars[self.q]; hl=bar.High-bar.Low
        if self.e1 is None: self.e1=hl; self.e2=hl
        else:
            self.e1=self.k*hl+(1-self.k)*self.e1
            self.e2=self.k*self.e1+(1-self.k)*self.e2
        if self.e2>0: self.mbuf.Add(self.e1/self.e2)
