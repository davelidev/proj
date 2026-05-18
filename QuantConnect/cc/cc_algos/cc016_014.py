from AlgorithmImports import *
class CC16_664(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(135,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _sk(self,h,n):
        s=h.iloc[-n:]; hi=float(s['high'].max()); lo=float(s['low'].min())
        cl=float(h['close'].iloc[-1]); return (cl-lo)/(hi-lo)*100 if hi>lo else 50
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,132,Resolution.Daily)
        if h.empty or len(h)<129: return
        k14=self._sk(h,14); k63=self._sk(h,63)
        # Oversold dip in quarterly uptrend → buy; overbought or trend break → sell
        if k63>50 and k14<20: st=1
        elif k63<50 or k14>80: st=0
        else: return
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
