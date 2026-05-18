from AlgorithmImports import *

class LRSlopeAndR2(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 60, Resolution.Daily)
        if h.empty or len(h)<60: return
        ys=[float(x) for x in h["close"].values]; n=len(ys)
        xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
        den_x=sum((xs[i]-mx)**2 for i in range(n))
        den_y=sum((ys[i]-my)**2 for i in range(n))
        if den_x<=0 or den_y<=0: return
        slope=num/den_x
        r2=(num**2)/(den_x*den_y)
        bull = slope > 0 and r2 > 0.5
        if bull:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
