from AlgorithmImports import *
class CC16_728(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(100,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,85,Resolution.Daily)
        if h.empty or len(h)<84: return
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        # current 20-day ROC vs rolling median of 20-day ROC over 63-day window
        roc_now=closes[-1]/closes[-21]-1
        rocs=[closes[i]/closes[i-21]-1 for i in range(21,len(closes))]
        if len(rocs)<1: return
        median_roc=sorted(rocs)[len(rocs)//2]
        # above-median momentum = strong regime
        st=1 if roc_now>median_roc else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
