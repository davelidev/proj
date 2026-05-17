from AlgorithmImports import *
class CC16_693(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(70,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,65,Resolution.Daily)
        if h.empty or len(h)<21: return
        p=self.Securities[self.qqq].Price
        # 20-day close high: price at or above recent 20-day close high = breakout (long)
        # 10-day close low: price at or below recent 10-day close low = breakdown (short → cash)
        c20h=float(h.iloc[-20:]['close'].max()); c10l=float(h.iloc[-10:]['close'].min())
        if p>=c20h: st=1
        elif p<=c10l: st=0
        else: return
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
