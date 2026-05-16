from AlgorithmImports import *

class IchimokuCloud(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol

        # Classic Hosoda parameters: 9, 26, 52
        self.ich = self.ICHIMOKU(self.qqq, 9, 26, 26, 52, 26, 26, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not self.ich.IsReady:
            return
        price = self.Securities[self.qqq].Price
        span_a = self.ich.SenkouA.Current.Value
        span_b = self.ich.SenkouB.Current.Value
        cloud_top    = max(span_a, span_b)
        cloud_bottom = min(span_a, span_b)

        if price > cloud_top:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        elif price < cloud_bottom:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
