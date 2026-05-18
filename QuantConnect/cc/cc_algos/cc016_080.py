from AlgorithmImports import *
class CC16_730(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(35,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,30,Resolution.Daily)
        if h.empty or len(h)<27: return
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        # 4 weekly (5-day) periods, at least 3 must be positive
        weeks=[closes[-1]>closes[-6], closes[-6]>closes[-11], closes[-11]>closes[-16], closes[-16]>closes[-21]]
        up_weeks=sum(weeks)
        st=1 if up_weeks>=3 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
