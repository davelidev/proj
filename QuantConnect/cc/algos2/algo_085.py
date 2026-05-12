from AlgorithmImports import *


class Algo085(QCAlgorithm):
    """
    Leveraged-Tech Basket EW + QQQ Trend Gate.

    Universe: 5 different 3x leveraged ETFs (TQQQ, TECL, SOXL, UPRO, FAS).
    Equal-weight basket (20% each, total = 100%) when QQQ > QQQ 200d SMA, else flat.
    Daily check; monthly rebalance back to 20% targets.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.basket = ["TQQQ", "TECL", "SOXL", "UPRO", "FAS"]
        self.symbols = []
        for t in self.basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.symbols.append(eq.Symbol)

        # QQQ for the trend signal
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.qqq_sma200 = self.SMA(self.qqq, 200, Resolution.Daily)

        self.SetWarmUp(220, Resolution.Daily)

        self._last_rebalance_month = -1

        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.DailyCheck,
        )

    def DailyCheck(self):
        if self.IsWarmingUp:
            return
        if not self.qqq_sma200.IsReady:
            return

        qqq_price = self.Securities[self.qqq].Price
        if qqq_price <= 0:
            return

        gate_on = qqq_price > self.qqq_sma200.Current.Value

        month = self.Time.month
        is_new_month = month != self._last_rebalance_month

        if not gate_on:
            # Flat: liquidate basket
            for sym in self.symbols:
                if self.Portfolio[sym].Invested:
                    self.SetHoldings(sym, 0.0)
            self._last_rebalance_month = month
            return

        # Gate on: equal-weight 20% each
        if is_new_month or self._needs_initial_fill():
            target = 1.0 / len(self.symbols)
            for sym in self.symbols:
                self.SetHoldings(sym, target)
            self._last_rebalance_month = month

    def _needs_initial_fill(self):
        for sym in self.symbols:
            if not self.Portfolio[sym].Invested:
                return True
        return False
