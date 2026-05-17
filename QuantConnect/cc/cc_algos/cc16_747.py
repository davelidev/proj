from AlgorithmImports import *
class CC16_747(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(260,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,270,Resolution.Daily)
        if h.empty or len(h)<252: return
        trs=[]
        for i in range(1,len(h)):
            hi=float(h['high'].iloc[i]); lo=float(h['low'].iloc[i]); pc=float(h['close'].iloc[i-1])
            trs.append(max(hi-lo,abs(hi-pc),abs(lo-pc)))
        if len(trs)<252: return
        atr14=sum(trs[-14:])/14
        # compare 14-day ATR to median of last 252 daily TRs
        median_tr=sorted(trs[-252:])[126]
        # below-median volatility = calm market = good for leveraged positions
        st=1 if atr14<median_tr else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
