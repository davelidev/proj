from AlgorithmImports import *


class Algo022(QCAlgorithm):
    """Trailing ATR-Stop on QQQ-trended TQQQ (peak - 4*ATR(14))."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.qqq_sma100 = self.SMA(self.qqq, 100, Resolution.Daily)
        self.tqqq_atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self.qqq_min30 = self.MIN(self.qqq, 30, Resolution.Daily)

        self.peak_price = 0.0
        self.in_position = False
        self.stopped_out = False

        self.SetWarmUp(120, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not (self.qqq_sma100.IsReady and self.tqqq_atr.IsReady and self.qqq_min30.IsReady):
            return

        qqq_price = self.Securities[self.qqq].Price
        tqqq_price = self.Securities[self.tqqq].Price
        sma100 = self.qqq_sma100.Current.Value
        atr = self.tqqq_atr.Current.Value
        recent_low = self.qqq_min30.Current.Value

        if self.in_position:
            if tqqq_price > self.peak_price:
                self.peak_price = tqqq_price
            stop_price = self.peak_price - 4 * atr
            if tqqq_price < stop_price:
                self.Liquidate()
                self.in_position = False
                self.stopped_out = True
                self.peak_price = 0.0
        else:
            uptrend = qqq_price > sma100
            recovered = recent_low > 0 and (qqq_price / recent_low - 1.0) >= 0.05
            can_enter = uptrend and (not self.stopped_out or recovered)
            if can_enter:
                self.SetHoldings(self.tqqq, 1.0)
                self.in_position = True
                self.stopped_out = False
                self.peak_price = tqqq_price
