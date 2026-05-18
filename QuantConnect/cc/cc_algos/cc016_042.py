from AlgorithmImports import *
class CC16_692(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(90,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,80,Resolution.Daily)
        if h.empty or len(h)<79: return
        p=self.Securities[self.qqq].Price
        # Senkou A from 26 periods ago
        t26h=float(h.iloc[-35:-26]['high'].max()); t26l=float(h.iloc[-35:-26]['low'].min())
        k26h=float(h.iloc[-52:-26]['high'].max()); k26l=float(h.iloc[-52:-26]['low'].min())
        senkou_a=(((t26h+t26l)/2)+((k26h+k26l)/2))/2
        # Senkou B: 52-period midpoint from 26 periods ago
        sb_h=float(h.iloc[-78:-26]['high'].max()); sb_l=float(h.iloc[-78:-26]['low'].min())
        senkou_b=(sb_h+sb_l)/2
        cloud_top=max(senkou_a,senkou_b)
        st=1 if p>cloud_top else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
