from AlgorithmImports import *


class Algo002(QCAlgorithm):
    """
    Algo #2 — RSI(2) MR + 200d SMA trend filter (on QQQ proxy).
    Only buy TQQQ dips when underlying QQQ is in uptrend (price > 200d SMA).
    Davey Cheat Code Strategy #1 + Chapter regime gate.

    Entry: QQQ price > 200d SMA AND RSI(2) on TQQQ < 10  -> 100% TQQQ
    Exit:  RSI(2) > 70 OR held >= 5 days OR QQQ < 200d SMA -> flat
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq  = self.AddEquity("QQQ",  Resolution.Daily).Symbol

        self.rsi  = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.sma  = self.SMA(self.qqq, 200, Resolution.Daily)
        self.SetWarmUp(220, Resolution.Daily)

        self.entry_bar  = None
        self.bar_count  = 0
        self.MAX_HOLD   = 5
        self.RSI_BUY    = 10
        self.RSI_SELL   = 70

        self.Schedule.On(
            self.DateRules.EveryDay(self.tqqq),
            self.TimeRules.AfterMarketOpen(self.tqqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.rsi.IsReady or not self.sma.IsReady:
            return

        self.bar_count += 1
        invested = self.Portfolio[self.tqqq].Invested
        rsi_val  = self.rsi.Current.Value
        qqq_px   = self.Securities[self.qqq].Price
        in_trend = qqq_px > self.sma.Current.Value

        if not invested:
            if in_trend and rsi_val < self.RSI_BUY:
                self.SetHoldings(self.tqqq, 1.0)
                self.entry_bar = self.bar_count
        else:
            held = self.bar_count - (self.entry_bar or self.bar_count)
            if rsi_val > self.RSI_SELL or held >= self.MAX_HOLD or not in_trend:
                self.Liquidate(self.tqqq)
                self.entry_bar = None
