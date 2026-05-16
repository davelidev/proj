from AlgorithmImports import *

class NR7_Median200_Filter(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi5=self.MAX(self.qqq, 5, Resolution.Daily); self.lo5=self.MIN(self.qqq, 5, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)
        self.nr7_h=None; self.nr7_l=None; self.armed=0

    def Rebalance(self):
        if self.IsWarmingUp or not (self.hi5.IsReady and self.lo5.IsReady): return
        h=self.History(self.qqq, 200, Resolution.Daily)
        if h.empty or len(h)<200: return
        c=[float(x) for x in h["close"].values]
        med=sorted(c)[100]
        in_trend=self.Securities[self.qqq].Price>med
        h2=self.History(self.qqq, 7, Resolution.Daily)
        if h2.empty or len(h2)<7: return
        ranges=[float(h2["high"].iloc[i])-float(h2["low"].iloc[i]) for i in range(7)]
        if ranges[-1] == min(ranges):
            self.nr7_h = float(h2["high"].iloc[-1])
            self.nr7_l = float(h2["low"].iloc[-1])
            self.armed = 3
        if self.nr7_h is None: return
        price=self.Securities[self.qqq].Price
        if not self.Portfolio[self.tqqq].Invested:
            if in_trend and price > self.nr7_h and self.armed > 0:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq, 1.0)
        else:
            if (not in_trend) or price <= self.lo5.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil, 1.0)
        self.armed = max(0, self.armed - 1)

    def OnData(self, data): pass
