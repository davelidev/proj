from AlgorithmImports import *
class CC17_052(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._n=30; self._obv=0.0; self._prev=None; self._st=None
        self._hist=[]; self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp: return
        bar=self.History(self.q,2,Resolution.Daily)
        if bar.empty or len(bar)<2: return
        cl=bar['close'].values; vol=bar['volume'].values
        if cl[1]>cl[0]: self._obv+=vol[1]
        elif cl[1]<cl[0]: self._obv-=vol[1]
        self._hist.append(self._obv)
        if len(self._hist)>self._n*2: self._hist=self._hist[-self._n*2:]
        if len(self._hist)<self._n: return
        avg=sum(self._hist[-self._n:])/self._n
        st=1 if self._obv>avg else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
