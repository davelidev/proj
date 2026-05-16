from AlgorithmImports import *

class HigherHighsHist(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.lo10=self.MIN(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady and self.lo10.IsReady): return
        h=self.History(self.qqq, 4, Resolution.Daily)
        if h.empty or len(h)<4: return
        c=[float(x) for x in h["close"].values]
        # higher closes: c[1]>c[0], c[2]>c[1], c[3]>c[2]
        higher = c[1]>c[0] and c[2]>c[1] and c[3]>c[2]
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend=self.Securities[self.qqq].Price>mid
        if not self.Portfolio[self.tqqq].Invested:
            if higher and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price<=self.lo10.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
