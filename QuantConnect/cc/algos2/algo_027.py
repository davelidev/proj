from AlgorithmImports import *


class Algo027(QCAlgorithm):
    """Triple-confirmation TQQQ entry with 30-day time-stop."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol

        self.qqq_sma50 = self.SMA(self.qqq, 50, Resolution.Daily)
        self.qqq_roc5 = self.ROC(self.qqq, 5, Resolution.Daily)
        self.qqq_rsi = self.RSI(self.qqq, 14, MovingAverageType.Wilders, Resolution.Daily)

        self.entry_date = None

        self.SetWarmUp(70, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not (self.qqq_sma50.IsReady and self.qqq_roc5.IsReady and self.qqq_rsi.IsReady):
            return

        price = self.Securities[self.qqq].Price
        sma = self.qqq_sma50.Current.Value
        roc5 = self.qqq_roc5.Current.Value
        rsi = self.qqq_rsi.Current.Value

        invested = self.Portfolio[self.tqqq].Invested

        # time-stop check first
        if invested and self.entry_date is not None:
            days_held = (self.Time - self.entry_date).days
            # ~30 trading days ≈ 42 calendar days; use trading-day approximation
            # We'll count business days conservatively as 30 calendar*1.4 ~ 42
            if days_held >= 42:
                self.Liquidate()
                self.entry_date = None
                return

        if not invested:
            cond_a = roc5 > 0
            cond_b = price > sma
            cond_c = 40 <= rsi <= 70
            if cond_a and cond_b and cond_c:
                self.SetHoldings(self.tqqq, 1.0)
                self.entry_date = self.Time
