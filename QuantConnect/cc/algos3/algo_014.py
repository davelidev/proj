from AlgorithmImports import *
import math


class Algo014(QCAlgorithm):
    """Volatility-targeted TQQQ: size = clip(0.35 / annualized_realized_vol_QQQ, 0, 1). Trade only when |dw|>0.05."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.target_vol = 0.35
        self.lookback = 20
        self.last_weight = 0.0

        self.SetWarmUp(40, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not data.ContainsKey(self.qqq):
            return

        hist = self.History(self.qqq, self.lookback + 5, Resolution.Daily)
        if hist is None or hist.empty:
            return
        try:
            closes = hist["close"]
        except Exception:
            return
        if len(closes) < self.lookback + 1:
            return

        log_returns = []
        for i in range(1, len(closes)):
            prev = closes.iloc[i - 1]
            cur = closes.iloc[i]
            if prev > 0 and cur > 0:
                log_returns.append(math.log(cur / prev))
        if len(log_returns) < self.lookback:
            return
        recent = log_returns[-self.lookback:]
        mean_r = sum(recent) / len(recent)
        var_r = sum((x - mean_r) ** 2 for x in recent) / (len(recent) - 1)
        std_daily = math.sqrt(var_r)
        ann_vol = std_daily * math.sqrt(252)
        if ann_vol <= 0:
            return

        w = self.target_vol / ann_vol
        if w < 0:
            w = 0.0
        if w > 1.0:
            w = 1.0

        if abs(w - self.last_weight) > 0.05:
            self.SetHoldings(self.tqqq, w)
            self.last_weight = w
