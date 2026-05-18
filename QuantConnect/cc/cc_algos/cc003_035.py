from AlgorithmImports import *

class DrawdownBuyTQQQ(QCAlgorithm):
    """Buy TQQQ when QQQ drops 12% from its 60-day high; exit when QQQ prints a new 60-day high."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        self.high60 = self.MAX(self.qqq, 60, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(75, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.high60.IsReady:
            return
        price = self.Securities[self.qqq].Price
        hi = self.high60.Current.Value
        dd = price / hi - 1.0  # negative when below high

        if not self.Portfolio[self.tqqq].Invested:
            if dd <= -0.12:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            # exit when QQQ prints a new 60-day high (price ≈ hi)
            if price >= hi * 0.999:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
