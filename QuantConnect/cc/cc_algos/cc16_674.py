from AlgorithmImports import *
class CC16_674(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(135,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,132,Resolution.Daily)
        if h.empty or len(h)<129: return
        cl=float(h['close'].iloc[-1])
        # Stoch(63) > 50 (quarterly uptrend)
        hi63=float(h.iloc[-63:]['high'].max()); lo63=float(h.iloc[-63:]['low'].min())
        k63=(cl-lo63)/(hi63-lo63)*100 if hi63>lo63 else 50
        # ROC(20) > 0 (short-term momentum)
        roc20=cl/float(h['close'].iloc[-21])-1
        st=1 if k63>50 and roc20>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
