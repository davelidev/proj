from AlgorithmImports import *
class CC19_013(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.P=20; self.thr=26.5
        self.k=2.0/10; self.e1=None; self.e2=None
        self.mbuf=RollingWindow[float](self.P+1)
        self.st=None; self.SetWarmUp(self.P+20,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self.mbuf.IsReady: return
        mi=sum(self.mbuf[i] for i in range(self.P))
        s=1 if mi<self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if not d.Bars.ContainsKey(self.q): return
        bar=d.Bars[self.q]; hl=bar.High-bar.Low
        if self.e1 is None: self.e1=hl; self.e2=hl
        else:
            self.e1=self.k*hl+(1-self.k)*self.e1
            self.e2=self.k*self.e1+(1-self.k)*self.e2
        if self.e2>0: self.mbuf.Add(self.e1/self.e2)
