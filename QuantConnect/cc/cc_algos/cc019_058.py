from AlgorithmImports import *
class CC19_058(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=10; self.thr=60.0
        self.cw=RollingWindow[float](self.n+1)
        self.st=None; self.SetWarmUp(self.n+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self.cw.IsReady: return
        pl=sum(1 for i in range(self.n) if self.cw[i]>self.cw[i+1])/self.n*100
        s=1 if pl>self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.cw.Add(d.Bars[self.q].Close)
