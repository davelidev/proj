from AlgorithmImports import *


class Algo089(QCAlgorithm):
    """
    TQQQ Dual-Trend + Volatility Squeeze Entry.

    Hold 100% TQQQ when:
        (a) QQQ > 100d SMA, AND
        (b) 20-day Bollinger Band width is in the lower half of its 252-day range
            (i.e. current bandwidth < median of last 252 daily bandwidths).
    Else flat.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.qqq_sma100 = self.SMA(self.qqq, 100, Resolution.Daily)
        self.qqq_bb = self.BB(self.qqq, 20, 2, MovingAverageType.Simple, Resolution.Daily)

        # Rolling window of bandwidth (relative width = (upper - lower) / middle)
        self.bw_window = RollingWindow[float](252)

        self.qqq_bb.Updated += self._on_bb_updated

        self.SetWarmUp(280, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.DailyCheck,
        )

    def _on_bb_updated(self, sender, updated):
        if not self.qqq_bb.IsReady:
            return
        upper = self.qqq_bb.UpperBand.Current.Value
        lower = self.qqq_bb.LowerBand.Current.Value
        mid = self.qqq_bb.MiddleBand.Current.Value
        if mid <= 0:
            return
        bw = (upper - lower) / mid
        self.bw_window.Add(bw)

    def DailyCheck(self):
        if self.IsWarmingUp:
            return
        if not self.qqq_sma100.IsReady or not self.qqq_bb.IsReady:
            return
        if self.bw_window.Count < 100:
            return

        qqq_price = self.Securities[self.qqq].Price
        if qqq_price <= 0:
            return

        trend_on = qqq_price > self.qqq_sma100.Current.Value

        # Current bandwidth
        upper = self.qqq_bb.UpperBand.Current.Value
        lower = self.qqq_bb.LowerBand.Current.Value
        mid = self.qqq_bb.MiddleBand.Current.Value
        if mid <= 0:
            return
        cur_bw = (upper - lower) / mid

        # Median of rolling window
        bws = sorted([self.bw_window[i] for i in range(self.bw_window.Count)])
        median_bw = bws[len(bws) // 2]

        squeeze_on = cur_bw < median_bw

        gate_on = trend_on and squeeze_on

        if gate_on and not self.Portfolio[self.tqqq].Invested:
            self.SetHoldings(self.tqqq, 1.0)
        elif (not gate_on) and self.Portfolio[self.tqqq].Invested:
            self.SetHoldings(self.tqqq, 0.0)
