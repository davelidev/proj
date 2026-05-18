from AlgorithmImports import *
class CC17_037(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._ema=self.EMA(self.q,14,Resolution.Daily)
        self._atr=self.ATR(self.q,10,MovingAverageType.Simple,Resolution.Daily)
        self._mult=1.5; self._st=None
        self.SetWarmUp(max(14,10)+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._ema.IsReady or not self._atr.IsReady: return
        mid=self._ema.Current.Value; atr=self._atr.Current.Value
        upper=mid+self._mult*atr
        p=self.Securities[self.q].Price
        st=1 if p>mid else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
