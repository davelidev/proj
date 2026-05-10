from AlgorithmImports import *


class Algo030(QCAlgorithm):
    """Tiered vol-filter TQQQ/TLT scale-out by QQQ 20d annualized vol."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tlt = self.AddEquity("TLT", Resolution.Daily).Symbol

        # STD of daily log/simple returns over 20 days
        self.qqq_ret_std = self.STD(self.qqq, 20, Resolution.Daily)
        # We need return-based STD, not price STD. Build a return series manually.
        self.return_window = RollingWindow[float](20)
        self.prev_price = None

        self.last_tier = None

        self.SetWarmUp(40, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        price = self.Securities[self.qqq].Price
        if price > 0 and self.prev_price is not None and self.prev_price > 0:
            ret = price / self.prev_price - 1.0
            self.return_window.Add(ret)
        if price > 0:
            self.prev_price = price

        if self.IsWarmingUp:
            return
        if not self.return_window.IsReady:
            return

        rets = [self.return_window[i] for i in range(self.return_window.Count)]
        n = len(rets)
        if n < 2:
            return
        mean = sum(rets) / n
        var = sum((r - mean) ** 2 for r in rets) / (n - 1)
        daily_std = var ** 0.5
        ann_vol = daily_std * (252 ** 0.5)

        if ann_vol < 0.15:
            tier = 1
        elif ann_vol < 0.25:
            tier = 2
        elif ann_vol < 0.40:
            tier = 3
        else:
            tier = 4

        if tier == self.last_tier:
            return

        if tier == 1:
            self.SetHoldings(self.tlt, 0.0)
            self.SetHoldings(self.tqqq, 1.0)
        elif tier == 2:
            self.SetHoldings(self.tqqq, 0.67)
            self.SetHoldings(self.tlt, 0.33)
        elif tier == 3:
            self.SetHoldings(self.tqqq, 0.33)
            self.SetHoldings(self.tlt, 0.67)
        else:
            self.SetHoldings(self.tqqq, 0.0)
            self.SetHoldings(self.tlt, 1.0)

        self.last_tier = tier
