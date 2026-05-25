from AlgorithmImports import *


class Algo056(QCAlgorithm):
    """#56 — %R(2)<-95 extreme MR + 150d trend filter."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.t = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.q = self.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.wpr = self.WILR(self.t, 2, Resolution.Daily)
        self.sma = self.SMA(self.q, 150, Resolution.Daily)
        self.SetWarmUp(170, Resolution.Daily)
        self.in_trend_pos = False
        self.in_mr_pos = False
        self.Schedule.On(self.DateRules.EveryDay(self.t),
                         self.TimeRules.AfterMarketOpen(self.t, 30), self.R)

    def R(self):
        if self.IsWarmingUp or not self.wpr.IsReady or not self.sma.IsReady: return
        v = self.wpr.Current.Value
        in_trend = self.Securities[self.q].Price > self.sma.Current.Value
        invested = self.Portfolio[self.t].Invested
        if in_trend:
            if not invested:
                self.SetHoldings(self.t, 1.0); self.in_trend_pos = True; self.in_mr_pos = False
        else:
            if self.in_trend_pos and invested:
                self.Liquidate(self.t); self.in_trend_pos = False
            if not invested and v < -95:
                self.SetHoldings(self.t, 1.0); self.in_mr_pos = True
            elif invested and self.in_mr_pos and v > -10:
                self.Liquidate(self.t); self.in_mr_pos = False
