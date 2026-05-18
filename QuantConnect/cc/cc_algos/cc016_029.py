from AlgorithmImports import *
class CC16_679(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1); self.SetEndDate(2025,12,31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self._st=None; self.SetWarmUp(70,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),self.TimeRules.AfterMarketOpen(self.qqq,30),self.Rebalance)
    def _obv(self,h):
        c=[float(x) for x in h['close'].values]; v=[float(x) for x in h['volume'].values]
        o=[0.0]
        for i in range(1,len(c)):
            if c[i]>c[i-1]: o.append(o[-1]+v[i])
            elif c[i]<c[i-1]: o.append(o[-1]-v[i])
            else: o.append(o[-1])
        return o
    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq,66,Resolution.Daily)
        if h.empty or len(h)<65: return
        cl=float(h['close'].iloc[-1])
        o=self._obv(h)
        obv_trend=o[-1]>o[-64]
        roc20=cl/float(h['close'].iloc[-21])-1
        st=1 if obv_trend and roc20>0 else 0
        if st==self._st: return
        self._st=st
        if st==1: self.SetHoldings(self.bil,0); self.SetHoldings(self.tqqq,1.0)
        else: self.SetHoldings(self.tqqq,0); self.SetHoldings(self.bil,1.0)
    def OnData(self,data): pass
