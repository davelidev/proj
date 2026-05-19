from AlgorithmImports import *
class CC19_061(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._lrs=self.LRS(self.q,20,Resolution.Daily)
        self._std=self.STD(self.q,20,Resolution.Daily)
        self.std_thr=0.0; self.st=None; self.SetWarmUp(20+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._lrs.IsReady or not self._std.IsReady: return
        slope=self._lrs.Current.Value; close=self.Securities[self.q].Price
        std_ok=True
        if self.std_thr>0:
            std_ok=(self._std.Current.Value/close if close>0 else 1)<self.std_thr
        s=1 if slope>0 and std_ok else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
