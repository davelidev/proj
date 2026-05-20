from AlgorithmImports import *

class QQQRangePosition(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi200=self.MAX(self.qqq,200,Resolution.Daily); self.lo200=self.MIN(self.qqq,200,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi200.IsReady and self.lo200.IsReady): return
        hi=self.hi200.Current.Value; lo=self.lo200.Current.Value; price=self.Securities[self.qqq].Price
        rng=hi-lo
        if rng<=0: return
        pos=(price-lo)/rng  # 0..1
        if pos > 0.5:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
