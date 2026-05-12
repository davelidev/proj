from AlgorithmImports import *
import math


class Algo086(QCAlgorithm):
    """
    Volatility-Targeted TQQQ Allocation.

    Single position TQQQ sized by volatility targeting.
    QQQ 20-day realized vol (annualized using daily log returns * sqrt(252)).
    Target portfolio vol = 30% annual. w = clip(0.30 / realized_vol, 0.0, 1.0).
    Daily rebalance, but only trade when |new_w - cur_w| > 5% to limit churn.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.target_vol = 0.30
        self.lookback = 20
        self.churn_threshold = 0.05

        self.SetWarmUp(self.lookback + 5, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.DailyRebalance,
        )

    def _realized_vol(self):
        history = self.History([self.qqq], self.lookback + 1, Resolution.Daily)
        if history.empty:
            return None
        try:
            closes = history.loc[self.qqq]["close"].values
        except Exception:
            return None
        if len(closes) < self.lookback + 1:
            return None

        log_rets = []
        for i in range(1, len(closes)):
            if closes[i - 1] > 0 and closes[i] > 0:
                log_rets.append(math.log(closes[i] / closes[i - 1]))
        if len(log_rets) < 2:
            return None

        mean = sum(log_rets) / len(log_rets)
        var = sum((r - mean) ** 2 for r in log_rets) / (len(log_rets) - 1)
        daily_vol = math.sqrt(var)
        ann_vol = daily_vol * math.sqrt(252)
        return ann_vol

    def DailyRebalance(self):
        if self.IsWarmingUp:
            return

        rv = self._realized_vol()
        if rv is None or rv <= 0:
            return

        new_w = self.target_vol / rv
        if new_w < 0.0:
            new_w = 0.0
        if new_w > 1.0:
            new_w = 1.0

        cur_w = self.Portfolio[self.tqqq].HoldingsValue / self.Portfolio.TotalPortfolioValue \
            if self.Portfolio.TotalPortfolioValue > 0 else 0.0

        if abs(new_w - cur_w) > self.churn_threshold:
            self.SetHoldings(self.tqqq, new_w)
