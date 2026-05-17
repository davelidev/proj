from AlgorithmImports import *
class CC16_724(QCAlgorithm):
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
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        rets=[closes[i]/closes[i-1]-1 for i in range(len(closes)-20,len(closes))]
        n=len(rets); mean=sum(rets)/n
        std=(sum((r-mean)**2 for r in rets)/n)**0.5
        if std==0: return
        # positive skewness = mean > median = more positive outliers = bullish
        med=sorted(rets)[n//2]
        skew=(mean-med)/std
        st=1 if skew>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
