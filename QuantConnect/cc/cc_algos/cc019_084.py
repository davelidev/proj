from AlgorithmImports import *
class CC19_084(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=13
        self.hw=RollingWindow[float](self.n)
        self.lw=RollingWindow[float](self.n)
        self.mode=None; self.syms=[]; self.st=None; self.SetWarmUp(self.n+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def R(self):
        if self.IsWarmingUp or not self.hw.IsReady or not self.syms: return
        sma_h=sum(self.hw[i] for i in range(self.n))/self.n
        sma_l=sum(self.lw[i] for i in range(self.n))/self.n
        close=self.Securities[self.q].Price
        if self.mode is None:
            self.mode='bull' if close>sma_h else 'bear'
        elif self.mode=='bull' and close<sma_l:
            self.mode='bear'
        elif self.mode=='bear' and close>sma_h:
            self.mode='bull'
        s=1 if self.mode=='bull' else 0
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
        if d.Bars.ContainsKey(self.q):
            self.hw.Add(d.Bars[self.q].High); self.lw.Add(d.Bars[self.q].Low)
