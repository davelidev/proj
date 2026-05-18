from AlgorithmImports import *
class CC17_003(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.q=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.t=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.b=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._adx=self.ADX(self.q,10,Resolution.Daily)
        self._n=10; self._st=None; self.SetWarmUp(20,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.q),self.TimeRules.AfterMarketOpen(self.q,30),self.R)
    def R(self):
        if self.IsWarmingUp or not self._adx.IsReady: return
        h=self.History(self.q,self._n+1,Resolution.Daily)
        if h.empty or len(h)<2: return
        trend_up=float(h["close"].iloc[-1])>float(h["close"].iloc[0])
        st=1 if self._adx.Current.Value>30 and trend_up else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.b,0); self.SetHoldings(self.t,1.0)
        else: self.SetHoldings(self.t,0); self.SetHoldings(self.b,1.0)
    def OnData(self,d): pass
