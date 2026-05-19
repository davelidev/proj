from AlgorithmImports import *
class CC19_046(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.ef=self.EMA(self.q,12,Resolution.Daily)
        self.es=self.EMA(self.q,26,Resolution.Daily)
        self.thr=0.0; self.st=None; self.SetWarmUp(26+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self.ef.IsReady or not self.es.IsReady: return
        es=self.es.Current.Value
        if es==0: return
        ppo=(self.ef.Current.Value-es)/es*100
        s=1 if ppo>self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
