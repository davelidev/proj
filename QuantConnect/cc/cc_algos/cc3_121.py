from AlgorithmImports import *

class HigherHighsStreak(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.closes=RollingWindow[float](4)
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.lo10=self.MIN(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def OnData(self, data):
        if self.qqq in data.Bars: self.closes.Add(data.Bars[self.qqq].Close)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.closes.IsReady and self.hi200.IsReady and self.lo200.IsReady and self.lo10.IsReady): return
        c0,c1,c2,c3=self.closes[0], self.closes[1], self.closes[2], self.closes[3]
        higher_highs = c0>c1 and c1>c2 and c2>c3
        mid=(self.hi200.Current.Value+self.lo200.Current.Value)/2.0
        in_trend=self.Securities[self.qqq].Price>mid
        if not self.Portfolio[self.tqqq].Invested:
            if higher_highs and in_trend:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if (not in_trend) or self.Securities[self.qqq].Price<=self.lo10.Current.Value*1.001:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
