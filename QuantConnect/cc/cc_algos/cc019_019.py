from AlgorithmImports import *
class CC19_019(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.n=40; self.sq=max(int(self.n**0.5),2)
        self.pw=RollingWindow[float](self.n+1)
        self.rbuf=RollingWindow[float](self.sq+1)
        self.prev=None; self.st=None; self.SetWarmUp(self.n+self.sq+10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def _wma(self,buf,p):
        vs=[buf[i] for i in range(p)]; denom=p*(p+1)//2
        return sum(vs[i]*(p-i) for i in range(p))/denom
    def R(self):
        if self.IsWarmingUp or not self.pw.IsReady: return
        wf=self._wma(self.pw,self.n); wh=self._wma(self.pw,self.n//2)
        raw=2*wh-wf
        self.rbuf.Add(raw)
        if not self.rbuf.IsReady: return
        hma=self._wma(self.rbuf,self.sq)
        rising=self.prev is not None and hma>self.prev
        self.prev=hma
        s=1 if rising else 0
        if s==self.st: return
        self.st=s
        if s: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d):
        if d.Bars.ContainsKey(self.q): self.pw.Add(d.Bars[self.q].Close)
