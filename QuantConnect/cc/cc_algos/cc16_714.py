from AlgorithmImports import *
class CC16_714(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(50,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _aroon(self,h,n):
        highs=[float(h['high'].iloc[i]) for i in range(len(h))]
        lows=[float(h['low'].iloc[i]) for i in range(len(h))]
        if len(highs)<n+1: return None
        window_h=highs[-(n+1):]; window_l=lows[-(n+1):]
        hi_idx=window_h.index(max(window_h)); lo_idx=window_l.index(min(window_l))
        return 100*hi_idx/n - 100*lo_idx/n
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,45,Resolution.Daily)
        if h.empty or len(h)<42: return
        aroon=self._aroon(h,40)
        if aroon is None: return
        st=1 if aroon>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
