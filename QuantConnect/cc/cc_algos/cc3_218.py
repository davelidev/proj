from AlgorithmImports import *

class LRChannelBreakout(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(120, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        h=self.History(self.qqq, 100, Resolution.Daily)
        if h.empty or len(h)<100: return
        ys=[float(x) for x in h["close"].values]; n=len(ys)
        xs=list(range(n)); mx=sum(xs)/n; my=sum(ys)/n
        num=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
        den=sum((xs[i]-mx)**2 for i in range(n))
        if den<=0: return
        slope=num/den; intercept=my-slope*mx
        # std error of residuals
        resid=[ys[i]-(intercept+slope*xs[i]) for i in range(n)]
        sd=(sum(r**2 for r in resid)/n)**0.5
        if sd<=0: return
        last_fit=intercept+slope*(n-1)
        upper=last_fit+sd; lower=last_fit-sd
        price=self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if price > upper:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if price < lower:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
