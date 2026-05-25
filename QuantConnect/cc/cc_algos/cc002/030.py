from AlgorithmImports import *


class Algo031(QCAlgorithm):
    """#31 — IBS extreme + ATR-based stop loss to limit catastrophic drawdowns."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr  = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(20, Resolution.Daily)
        self.entry_price = None
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30),
                         self.Rebalance)

    def Rebalance(self):
        if self.IsWarmingUp or not self.atr.IsReady: return
        bar = self.Securities[self.tqqq]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        invested = self.Portfolio[self.tqqq].Invested
        atr = self.atr.Current.Value

        if not invested and ibs < 0.1:
            self.SetHoldings(self.tqqq, 1.0)
            self.entry_price = c
        elif invested:
            stop = self.entry_price - 3.0 * atr if self.entry_price else 0
            if ibs > 0.9 or c < stop:
                self.Liquidate(self.tqqq)
                self.entry_price = None
