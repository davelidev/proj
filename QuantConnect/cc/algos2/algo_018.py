from AlgorithmImports import *
import math


class Algo018(QCAlgorithm):
    """TQQQ gated by 60d realized skew of QQQ daily returns: skew > +0.5 → 100% TQQQ; else flat. Monthly recheck."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.skew_window = 60
        self.threshold = 0.5
        self.in_position = False

        self.Schedule.On(
            self.DateRules.MonthStart(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

        self.SetWarmUp(80, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        hist = self.History(self.qqq, self.skew_window + 5, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < self.skew_window + 1:
            return

        rets = []
        for i in range(1, len(closes)):
            prev = closes.iloc[i - 1]
            cur = closes.iloc[i]
            if prev > 0:
                rets.append((cur / prev) - 1.0)
        if len(rets) < self.skew_window:
            return
        recent = rets[-self.skew_window:]
        n = len(recent)
        mean_r = sum(recent) / n
        var_r = sum((x - mean_r) ** 2 for x in recent) / (n - 1)
        std_r = math.sqrt(var_r)
        if std_r <= 0:
            return
        skew = sum(((x - mean_r) / std_r) ** 3 for x in recent) / n

        want_in = skew > self.threshold
        if want_in and not self.in_position:
            self.SetHoldings(self.tqqq, 1.0)
            self.in_position = True
        elif not want_in and self.in_position:
            self.Liquidate()
            self.in_position = False
