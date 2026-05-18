from AlgorithmImports import *

class DualLRSlope(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily); self.state=None

    def _slope(self, ys):
        n=len(ys); xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
        den=sum((xs[i]-mx)**2 for i in range(n))
        return num/den if den>0 else 0.0

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 100, Resolution.Daily)
        if h.empty or len(h)<100: return
        c=[float(x) for x in h["close"].values]
        s_long=self._slope(c[-100:])
        s_short=self._slope(c[-20:])
        l_bull = s_long > 0
        s_bull = s_short > 0
        if l_bull and s_bull: ns,wt,wb="BULL",1.0,0.0
        elif l_bull or s_bull: ns,wt,wb="MIXED",0.5,0.5
        else: ns,wt,wb="BEAR",0.0,1.0
        if ns!=self.state:
            self.SetHoldings(self.tqqq,wt); self.SetHoldings(self.bil,wb); self.state=ns

    def OnData(self, data): pass
