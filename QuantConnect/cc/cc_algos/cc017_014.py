from AlgorithmImports import *
class CC17_014(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._atr=self.ATR(self.q,14,MovingAverageType.Simple,Resolution.Daily)
        self._ch=30; self._mult=1.2; self._st=None
        self.SetWarmUp(max(14,30)+5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._atr.IsReady: return
        h=self.History(self.q,self._ch+1,Resolution.Daily)
        if h.empty or len(h)<self._ch: return
        hi=float(h['high'].iloc[:-1].max())
        p=self.Securities[self.q].Price
        atr=self._atr.Current.Value
        st=1 if p>hi-self._mult*atr else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
