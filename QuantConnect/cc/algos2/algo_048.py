from AlgorithmImports import *


class Algo048(QCAlgorithm):
    """#48 — #46 (winner) variants on QLD (2x) instead of TQQQ — should reduce DD."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qld  = self.AddEquity("QLD",  Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 150, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.in_trend_pos = False
        self.in_mr_pos = False
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady: return
        bar = self.Securities[self.qld]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        invested = self.Portfolio[self.qld].Invested
        if in_trend:
            if not invested:
                self.SetHoldings(self.qld, 1.0); self.in_trend_pos = True; self.in_mr_pos = False
        else:
            if self.in_trend_pos and invested:
                self.Liquidate(self.qld); self.in_trend_pos = False
            if not invested and ibs < 0.05:
                self.SetHoldings(self.qld, 1.0); self.in_mr_pos = True
            elif invested and self.in_mr_pos and ibs > 0.7:
                self.Liquidate(self.qld); self.in_mr_pos = False
