from AlgorithmImports import *


class Algo049(QCAlgorithm):
    """#49 — TQQQ + 5-day low pullback within 100d uptrend."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 100, Resolution.Daily)
        self.min5 = self.MIN(self.tqqq, 5, Resolution.Daily)
        self.SetWarmUp(120, Resolution.Daily)
        self.entry_bar = None
        self.bar_count = 0
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.min5.IsReady: return
        self.bar_count += 1
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        c = self.Securities[self.tqqq].Price
        is_5d_low = c <= self.min5.Current.Value
        invested = self.Portfolio[self.tqqq].Invested
        if not invested and in_trend and is_5d_low:
            self.SetHoldings(self.tqqq, 1.0)
            self.entry_bar = self.bar_count
        elif invested:
            held = self.bar_count - (self.entry_bar or self.bar_count)
            if held >= 5 or not in_trend:
                self.Liquidate(self.tqqq)
                self.entry_bar = None
