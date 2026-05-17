from AlgorithmImports import *
class CC16_736(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,25,Resolution.Daily)
        if h.empty or len(h)<22: return
        # count days with higher-high AND higher-low = pure uptrend day
        trend_days=sum(1 for i in range(len(h)-20,len(h))
                      if float(h['high'].iloc[i])>float(h['high'].iloc[i-1])
                      and float(h['low'].iloc[i])>float(h['low'].iloc[i-1]))
        st=1 if trend_days>10 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
