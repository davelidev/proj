from AlgorithmImports import *
class CC15_604(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._roc20=self.ROC("QQQ",20,Resolution.Daily)
        self._roc60=self.ROC("QQQ",60,Resolution.Daily)
        self.SetWarmUp(70,Resolution.Daily); self._st=None
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp or not self._roc20.IsReady or not self._roc60.IsReady: return
        both_pos=self._roc20.Current.Value>0 and self._roc60.Current.Value>0
        either_neg=self._roc20.Current.Value<0 or self._roc60.Current.Value<0
        if both_pos: st=1
        elif either_neg: st=0
        else: return
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
