from AlgorithmImports import *
class CC16_669(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._adx=self.ADX(self.qqq,14,Resolution.Daily)
        self._st=None; self.SetWarmUp(30,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp or not self._adx.IsReady: return
        adx=self._adx.Current.Value
        dip=self._adx.PositiveDirectionalIndex.Current.Value
        dim=self._adx.NegativeDirectionalIndex.Current.Value
        h=self.History(self.qqq,22,Resolution.Daily)
        if h.empty or len(h)<21: return
        roc20=float(h['close'].iloc[-1])/float(h['close'].iloc[0])-1
        st=1 if adx>20 and dip>dim and roc20>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
