from AlgorithmImports import *
class CC19_088(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.k=2.0/(21+1); self.thr=0.6
        self.em=None; self.ei=None; self.prev=None
        self.st=None; self.SetWarmUp(21+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or self.em is None or self.ei is None: return
        denom=self.em+self.ei
        dem=self.em/denom if denom>0 else 0.5
        s=1 if dem>self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if not d.Bars.ContainsKey(self.q): return
        bar=d.Bars[self.q]
        if self.prev is not None:
            dm=max(bar.High-self.prev.High,0)
            di=max(self.prev.Low-bar.Low,0)
            if self.em is None: self.em=dm; self.ei=di
            else:
                self.em=self.k*dm+(1-self.k)*self.em
                self.ei=self.k*di+(1-self.k)*self.ei
        self.prev=bar
