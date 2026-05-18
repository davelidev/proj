from AlgorithmImports import *
class CC16_663(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(135,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _skd(self,h,n):
        k_vals=[]
        for i in range(3):
            s=h.iloc[-(n+i):-i] if i>0 else h.iloc[-n:]
            hi=float(s['high'].max()); lo=float(s['low'].min())
            c=float(h['close'].iloc[-(i+1)])
            k_vals.append((c-lo)/(hi-lo)*100 if hi>lo else 50)
        return k_vals[0], sum(k_vals)/3
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,132,Resolution.Daily)
        if h.empty or len(h)<129: return
        k14,d14=self._skd(h,14); _,d63=self._skd(h,63)
        # K/D crossover in long-term uptrend
        st=1 if k14>d14 and d63>50 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
