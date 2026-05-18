from AlgorithmImports import *
class CC16_695(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.spy=self.AddEquity("SPY",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(70,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq,65,Resolution.Daily)
        hs=self.History(self.spy,65,Resolution.Daily)
        if hq.empty or len(hq)<64 or hs.empty or len(hs)<64: return
        rq=float(hq['close'].iloc[-1])/float(hq['close'].iloc[0])-1
        rs=float(hs['close'].iloc[-1])/float(hs['close'].iloc[0])-1
        st=1 if rq>rs else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
