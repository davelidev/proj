from AlgorithmImports import *
class CC16_686(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._cci=self.CCI(self.qqq,20,MovingAverageType.Simple,Resolution.Daily)
        self._st=None; self.SetWarmUp(70,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _atr(self,h,n):
        trs=[]
        for i in range(1,len(h)):
            hi=float(h['high'].iloc[i]); lo=float(h['low'].iloc[i]); pc=float(h['close'].iloc[i-1])
            trs.append(max(hi-lo,abs(hi-pc),abs(lo-pc)))
        return sum(trs[-n:])/n if len(trs)>=n else None
    def Rebalance(self):
        if self.IsWarmingUp or not self._cci.IsReady: return
        h=self.History(self.qqq,70,Resolution.Daily)
        if h.empty or len(h)<65: return
        atr14=self._atr(h,14); atr63=self._atr(h,63)
        if atr14 is None or atr63 is None: return
        low_vol=atr14<atr63*1.5
        cci=self._cci.Current.Value
        st=1 if cci>0 and low_vol else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
