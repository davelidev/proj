from AlgorithmImports import *

class Donchian60BreakoutMid(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi60=self.MAX(self.qqq,60,Resolution.Daily); self.lo60=self.MIN(self.qqq,60,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not(self.hi60.IsReady and self.lo60.IsReady): return
        price=self.Securities[self.qqq].Price
        mid=(self.hi60.Current.Value+self.lo60.Current.Value)/2.0
        if not self.Portfolio[self.tqqq].Invested:
            if price>=self.hi60.Current.Value*0.999:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if price<mid:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
