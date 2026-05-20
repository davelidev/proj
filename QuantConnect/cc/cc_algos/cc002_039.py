from AlgorithmImports import *


class Algo042(QCAlgorithm):
    """#42 — #40 (SMA150 hybrid) + ATR stop on MR positions only."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.sma  = self.SMA(self.qqq, 150, Resolution.Daily)
        self.atr  = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.in_trend_pos = False
        self.in_mr_pos = False
        self.entry_price = None
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.atr.IsReady: return
        bar = self.Securities[self.tqqq]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        in_trend = self.Securities[self.qqq].Price > self.sma.Current.Value
        invested = self.Portfolio[self.tqqq].Invested
        atr_v = self.atr.Current.Value

        if in_trend:
            if not invested:
                self.SetHoldings(self.tqqq, 1.0)
                self.in_trend_pos = True
                self.in_mr_pos = False
        else:
            if self.in_trend_pos and invested:
                self.Liquidate(self.tqqq)
                self.in_trend_pos = False
            if not invested and ibs < 0.05:
                self.SetHoldings(self.tqqq, 1.0)
                self.in_mr_pos = True
                self.entry_price = c
            elif invested and self.in_mr_pos:
                stop = self.entry_price - 3.0 * atr_v if self.entry_price else 0
                if ibs > 0.9 or c < stop:
                    self.Liquidate(self.tqqq)
                    self.in_mr_pos = False
                    self.entry_price = None
