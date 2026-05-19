from AlgorithmImports import *
class CC19_053(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=20; self.thr=60.0
        self._sma=self.SMA(self.q,self.n,Resolution.Daily)
        self.cw=RollingWindow[float](self.n)
        self.st=None; self.SetWarmUp(self.n+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._sma.IsReady or not self.cw.IsReady: return
        sma=self._sma.Current.Value
        tii=sum(1 for i in range(self.n) if self.cw[i]>sma)/self.n*100
        s=1 if tii>self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.cw.Add(d.Bars[self.q].Close)
