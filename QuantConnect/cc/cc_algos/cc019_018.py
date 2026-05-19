from AlgorithmImports import *
class CC19_018(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.UniverseSettings.Resolution=Resolution.Daily
        self.AddUniverse(self.CoarseSelection,self.FineSelection)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=20; self.sq=max(int(self.n**0.5),2)
        self.pw=RollingWindow[float](self.n+1)
        self.rbuf=RollingWindow[float](self.sq+1)
        self.prev=None; self.syms=[]; self.st=None; self.SetWarmUp(self.n+self.sq+100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def CoarseSelection(self,c):
        return [x.Symbol for x in sorted(c,key=lambda x:x.DollarVolume,reverse=True)[:100]]
    def FineSelection(self,f):
        self.syms=[x.Symbol for x in sorted(f,key=lambda x:x.MarketCap,reverse=True)[:5]]; return self.syms
    def _wma(self,buf,p):
        vs=[buf[i] for i in range(p)]; denom=p*(p+1)//2
        return sum(vs[i]*(p-i) for i in range(p))/denom
    def R(self):
        if self.IsWarmingUp or not self.pw.IsReady or not self.syms: return
        wf=self._wma(self.pw,self.n); wh=self._wma(self.pw,self.n//2)
        raw=2*wh-wf
        self.rbuf.Add(raw)
        if not self.rbuf.IsReady: return
        hma=self._wma(self.rbuf,self.sq)
        rising=self.prev is not None and hma>self.prev
        self.prev=hma
        s=1 if rising else 0
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
        if d.Bars.ContainsKey(self.q): self.pw.Add(d.Bars[self.q].Close)
