from AlgorithmImports import *
class CC19_076(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.k1=2.0/(35+1); self.k2=2.0/(20+1); self.ks=2.0/(10+1)
        self.e1=None; self.e2=None; self.sig=None; self.prev_c=None
        self.use_sig=True; self.st=None; self.SetWarmUp(35+20+10+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or self.e2 is None: return
        s=1 if (self.e2>self.sig if self.use_sig and self.sig is not None else self.e2>0) else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if not d.Bars.ContainsKey(self.q): return
        c=d.Bars[self.q].Close
        if self.prev_c is not None and self.prev_c>0:
            roc=(c/self.prev_c-1)*100
            if self.e1 is None: self.e1=roc; self.e2=roc; self.sig=roc
            else:
                self.e1=self.k1*roc+(1-self.k1)*self.e1
                self.e2=self.k2*self.e1+(1-self.k2)*self.e2
                if self.sig is None: self.sig=self.e2
                else: self.sig=self.ks*self.e2+(1-self.ks)*self.sig
        self.prev_c=c
