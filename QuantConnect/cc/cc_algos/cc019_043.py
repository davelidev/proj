from AlgorithmImports import *
import math
class CC19_043(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.sp=10; self.lp=30; self.thr=1.0
        self.closes=RollingWindow[float](self.lp+2)
        self.st=None; self.SetWarmUp(self.lp+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def _hv(self,p):
        if not self.closes.IsReady: return None
        rets=[math.log(self.closes[i]/self.closes[i+1]) for i in range(p) if self.closes[i+1]>0]
        if len(rets)<2: return None
        m=sum(rets)/len(rets); v=sum((r-m)**2 for r in rets)/(len(rets)-1)
        return math.sqrt(v*252)
    def R(self):
        if self.IsWarmingUp or not self.closes.IsReady: return
        hvs=self._hv(self.sp); hvl=self._hv(self.lp)
        if hvs is None or hvl is None or hvl==0: return
        s=1 if hvs/hvl<self.thr else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.closes.Add(d.Bars[self.q].Close)
