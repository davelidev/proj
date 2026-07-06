from AlgorithmImports import *
class TII50Bull(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._sma=self.SMA(self.qqq,50,Resolution.Daily)
        self.closes=RollingWindow[float](50)
        self._st=None; self.SetWarmUp(60,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp or not self._sma.IsReady or not self.closes.IsReady: return
        sma=self._sma.Current.Value
        tii=sum(1 for i in range(50) if self.closes[i]>sma)
        st=1 if tii>25 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data):
        if data.Bars.ContainsKey(self.qqq): self.closes.Add(data.Bars[self.qqq].Close)
