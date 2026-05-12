from AlgorithmImports import *


class Algo001(QCAlgorithm):
    """
    Algo #1 — RSI(2) Mean Reversion on TQQQ
    Davey Cheat Code Strategy #1 (Short Term RSI).

    Entry: RSI(2) < 10 (oversold) -> 100% TQQQ
    Exit:  RSI(2) > 70 OR held >= 5 days -> flat (cash)
    Resolution: Daily.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi  = self.RSI(self.tqqq, 2, MovingAverageType.Wilders, Resolution.Daily)
        self.SetWarmUp(20, Resolution.Daily)

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
        if self.IsWarmingUp or not self.rsi.IsReady:
            return

        self.bar_count += 1
        invested = self.Portfolio[self.tqqq].Invested
        rsi_val  = self.rsi.Current.Value

        if not invested:
            if rsi_val < self.RSI_BUY:
                self.SetHoldings(self.tqqq, 1.0)
                self.entry_bar = self.bar_count
        else:
            held = self.bar_count - (self.entry_bar or self.bar_count)
            if rsi_val > self.RSI_SELL or held >= self.MAX_HOLD:
                self.Liquidate(self.tqqq)
                self.entry_bar = None
