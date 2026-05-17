from AlgorithmImports import *
class CC16_708(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.gld=self.AddEquity("GLD",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        hq=self.History(self.qqq,25,Resolution.Daily)
        hg=self.History(self.gld,25,Resolution.Daily)
        if hq.empty or len(hq)<22 or hg.empty or len(hg)<22: return
        rq=float(hq['close'].iloc[-1])/float(hq['close'].iloc[-21])-1
        rg=float(hg['close'].iloc[-1])/float(hg['close'].iloc[-21])-1
        # tech outperforming gold = risk-on = growth regime
        st=1 if rq>rg else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
