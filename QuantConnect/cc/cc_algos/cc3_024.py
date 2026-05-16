from AlgorithmImports import *

class Donchian200VIXFilter(QCAlgorithm):
    """Donchian-200 midline trend + VIX panic exit."""
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.bil  = self.AddEquity("BIL",  Resolution.Daily).Symbol
        self.vix  = self.AddData(CBOE, "VIX", Resolution.Daily).Symbol

        self.high = self.MAX(self.qqq, 200, Resolution.Daily)
        self.low  = self.MIN(self.qqq, 200, Resolution.Daily)

        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)
        self.SetWarmUp(220, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp or not (self.high.IsReady and self.low.IsReady and self.Securities.ContainsKey(self.vix)):
            return
        midline = (self.high.Current.Value + self.low.Current.Value) / 2.0
        price = self.Securities[self.qqq].Price
        vix_val = self.Securities[self.vix].Price

        if price > midline and vix_val < 30:
            if not self.Portfolio[self.tqqq].Invested:
                self.Liquidate(self.bil)
                self.SetHoldings(self.tqqq, 1.0)
        else:
            if not self.Portfolio[self.bil].Invested:
                self.Liquidate(self.tqqq)
                self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
