from AlgorithmImports import *


class Algo066(QCAlgorithm):
    """#66 — TQQQ + SMA200 + IBS<0.05 hybrid + 3xATR stop on MR pos."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.s = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.s, 200, Resolution.Daily)
        self.atr = self.ATR(self.s, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)
        self.in_trend_pos = False
        self.in_mr_pos = False
        self.entry_price = None
        self.Schedule.On(self.DateRules.EveryDay(self.s),
                         self.TimeRules.AfterMarketOpen(self.s, 30), self.R)

    def R(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.atr.IsReady: return
        bar = self.Securities[self.s]
        h, l, c = bar.High, bar.Low, bar.Close
        if h <= l: return
        ibs = (c - l) / (h - l)
        in_trend = c > self.sma.Current.Value
        invested = self.Portfolio[self.s].Invested
        atr_v = self.atr.Current.Value

        if in_trend:
            if not invested:
                self.SetHoldings(self.s, 1.0); self.in_trend_pos = True; self.in_mr_pos = False
        else:
            if self.in_trend_pos and invested:
                self.Liquidate(self.s); self.in_trend_pos = False
            if not invested and ibs < 0.05:
                self.SetHoldings(self.s, 1.0); self.in_mr_pos = True; self.entry_price = c
            elif invested and self.in_mr_pos:
                stop = self.entry_price - 3.0 * atr_v if self.entry_price else 0
                if ibs > 0.7 or c < stop:
                    self.Liquidate(self.s); self.in_mr_pos = False; self.entry_price = None
