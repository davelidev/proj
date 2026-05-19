from AlgorithmImports import *
class CC19_007(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=14; self.delay=self.n//2+1
        self._sma=self.SMA(self.q,self.n,Resolution.Daily)
        self._sw=RollingWindow[float](self.delay+1)
        self.st=None; self.SetWarmUp(self.n+self.delay+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._sma.IsReady or not self._sw.IsReady: return
        dpo=self.Securities[self.q].Price-self._sw[self.delay]
        s=1 if dpo>0 else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if self._sma.IsReady: self._sw.Add(self._sma.Current.Value)
