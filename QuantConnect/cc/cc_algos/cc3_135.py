from AlgorithmImports import *

class QQQ10dayDip10pct(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100000)
        self.qqq=self.AddEquity("QQQ",Resolution.Daily).Symbol
        self.tqqq=self.AddEquity("TQQQ",Resolution.Daily).Symbol
        self.bil=self.AddEquity("BIL",Resolution.Daily).Symbol
        self.hi10=self.MAX(self.qqq,10,Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq), self.TimeRules.AfterMarketOpen(self.qqq,30), self.Rebalance)
        self.SetWarmUp(20, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.hi10.IsReady: return
        price=self.Securities[self.qqq].Price
        dd=price/self.hi10.Current.Value-1.0
        if not self.Portfolio[self.tqqq].Invested:
            if dd<=-0.10:
                self.Liquidate(self.bil); self.SetHoldings(self.tqqq,1.0)
        else:
            if price>=self.hi10.Current.Value*0.999:
                self.Liquidate(self.tqqq); self.SetHoldings(self.bil,1.0)

    def OnData(self, data): pass
