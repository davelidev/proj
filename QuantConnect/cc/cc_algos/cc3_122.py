from AlgorithmImports import *

class ThreeDownDaysHist(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.hi5=self.MAX(self.qqq,5,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady and self.hi5.IsReady): return
        h=self.History(self.qqq, 4, Resolution.Daily)
        if h.empty or len(h)<4: return
        c=[float(x) for x in h["close"].values]
        oversold = c[0]>c[1] and c[1]>c[2] and c[2]>c[3]  # history is oldest..newest
        # wait actually history returns oldest..newest so check the other direction
        # c[0] oldest, c[-1] newest. 3 down days = c[3]<c[2]<c[1]<c[0]
        oversold = c[3]<c[2] and c[2]<c[1] and c[1]<c[0]
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend = self.Securities[self.qqq].Price > mid
        if not self.Portfolio[self.tqqq].Invested:
            if in_trend and oversold:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price >= self.hi5.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
