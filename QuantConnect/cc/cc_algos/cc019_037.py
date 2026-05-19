from AlgorithmImports import *
class CC19_037(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=5; self.thr=0.0
        self.bars=RollingWindow[TradeBar](self.n)
        self.st=None; self.SetWarmUp(self.n+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def _bop(self):
        total=0
        for i in range(self.n):
            bar=self.bars[i]; hl=bar.High-bar.Low
            total+=((bar.Close-bar.Open)/hl if hl>0 else 0)
        return total/self.n
    def R(self):
        if self.IsWarmingUp or not self.bars.IsReady: return
        s=1 if self._bop()>self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.bars.Add(d.Bars[self.q])
