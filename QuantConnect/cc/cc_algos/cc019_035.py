from AlgorithmImports import *
class CC19_035(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=14; self.use_sig=False
        self.bars=RollingWindow[TradeBar](self.n+3)
        self.rvibuf=RollingWindow[float](4)
        self.syms=[]; self.st=None; self.SetWarmUp(self.n+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def _rvi(self):
        n=self.n
        num=sum(((self.bars[i].Close-self.bars[i].Open)+(2*(self.bars[i+1].Close-self.bars[i+1].Open))+(2*(self.bars[i+2].Close-self.bars[i+2].Open))+(self.bars[i+3].Close-self.bars[i+3].Open)) for i in range(n))/n
        den=sum(((self.bars[i].High-self.bars[i].Low)+(2*(self.bars[i+1].High-self.bars[i+1].Low))+(2*(self.bars[i+2].High-self.bars[i+2].Low))+(self.bars[i+3].High-self.bars[i+3].Low)) for i in range(n))/n
        return num/den if den!=0 else 0
    def R(self):
        if self.IsWarmingUp or not self.bars.IsReady or not self.syms: return
        rvi=self._rvi()
        self.rvibuf.Add(rvi)
        if self.use_sig and self.rvibuf.IsReady:
            sig=(self.rvibuf[0]+2*self.rvibuf[1]+2*self.rvibuf[2]+self.rvibuf[3])/6
            s=1 if rvi>sig else 0
        else:
            s=1 if rvi>0 else 0
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
        if d.Bars.ContainsKey(self.q): self.bars.Add(d.Bars[self.q])
