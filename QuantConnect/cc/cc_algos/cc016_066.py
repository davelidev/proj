from AlgorithmImports import *
class CC16_716(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _lr_slope(self,closes,n):
        c=closes[-n:]
        sx=sum(range(n)); sy=sum(c)
        sxx=sum(i*i for i in range(n)); sxy=sum(i*y for i,y in enumerate(c))
        denom=n*sxx-sx*sx
        return 0 if denom==0 else (n*sxy-sx*sy)/denom
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,25,Resolution.Daily)
        if h.empty or len(h)<22: return
        closes=[float(h['close'].iloc[i]) for i in range(len(h))]
        slope=self._lr_slope(closes,20)
        # positive linear regression slope = upward price trajectory
        st=1 if slope>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
