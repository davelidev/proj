from AlgorithmImports import *
import math
class CC19_001(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=14; self.thr=38.2
        self.bars=RollingWindow[TradeBar](self.n+1)
        self.st=None; self.SetWarmUp(self.n+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def _ci(self):
        n=self.n; b=[self.bars[i] for i in range(n+1)]
        hh=max(x.High for x in b[:n]); ll=min(x.Low for x in b[:n])
        if hh<=ll: return 100.0
        tr=sum(max(b[i].High,b[i+1].Close)-min(b[i].Low,b[i+1].Close) for i in range(n))
        return 100*math.log10(tr/(hh-ll))/math.log10(n)
    def R(self):
        if self.IsWarmingUp or not self.bars.IsReady: return
        s=1 if self._ci()<self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.bars.Add(d.Bars[self.q])
