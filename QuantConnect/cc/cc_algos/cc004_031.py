from AlgorithmImports import *

class RegimeGatedDrawdownBuy(QCAlgorithm):
    """Buy TQQQ on 12% drop from 60-day high ONLY when QQQ > 200d Donchian midline; exit on new high."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.high60 = self.MAX(self.qqq, 60, Resolution.Daily)
        self.hi200 = self.MAX(self.qqq, 200, Resolution.Daily)
        self.lo200 = self.MIN(self.qqq, 200, Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high60.IsReady and self.hi200.IsReady and self.lo200.IsReady):
            return
        price = self.Securities[self.qqq].Price
        hi60 = self.high60.Current.Value
        mid = (self.hi200.Current.Value + self.lo200.Current.Value) / 2.0
        in_trend = price > mid
        dd = price / hi60 - 1.0  # negative when below high

        if not self.Portfolio[self.tqqq].Invested:
            if in_trend and dd <= -0.12:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if price >= hi60 * 0.999 or not in_trend:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data): pass
