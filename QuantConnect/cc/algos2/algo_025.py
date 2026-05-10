from AlgorithmImports import *


class Algo025(QCAlgorithm):
    """TQQQ with 6-month drawdown stop and 60-day cooldown."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.tqqq_max126 = self.MAX(self.tqqq, 126, Resolution.Daily)
        # 30-day-ago price via History — keep a small rolling list ourselves
        self.price_history = RollingWindow[float](40)

        self.in_cooldown = False
        self.cooldown_start = None

        self.SetWarmUp(150, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.tqqq),
            self.TimeRules.AfterMarketOpen(self.tqqq, 30),
            self.Rebalance,
        )

    def Rebalance(self):
        price = self.Securities[self.tqqq].Price
        if price > 0:
            self.price_history.Add(price)

        if self.IsWarmingUp:
            return
        if not self.tqqq_max126.IsReady:
            return

        peak = self.tqqq_max126.Current.Value
        dd = 0.0 if peak == 0 else (price - peak) / peak

        if not self.in_cooldown:
            if dd < -0.30:
                self.Liquidate()
                self.in_cooldown = True
                self.cooldown_start = self.Time
                return
            if not self.Portfolio[self.tqqq].Invested:
                self.SetHoldings(self.tqqq, 1.0)
        else:
            days_in_cd = (self.Time - self.cooldown_start).days
            if days_in_cd >= 60 and self.price_history.Count >= 31:
                price_30d_ago = self.price_history[30]
                if price > price_30d_ago:
                    self.in_cooldown = False
                    self.cooldown_start = None
                    self.SetHoldings(self.tqqq, 1.0)
