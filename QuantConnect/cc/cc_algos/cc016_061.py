from AlgorithmImports import *
class CC16_711(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(40,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _cmo(self,h,n):
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        changes=[closes[i]-closes[i-1] for i in range(1,len(closes))]
        if len(changes)<n: return None
        ups=sum(c for c in changes[-n:] if c>0)
        downs=sum(abs(c) for c in changes[-n:] if c<0)
        total=ups+downs
        return 0 if total==0 else 100*(ups-downs)/total
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,38,Resolution.Daily)
        if h.empty or len(h)<33: return
        cmo=self._cmo(h,30)
        if cmo is None: return
        st=1 if cmo>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
