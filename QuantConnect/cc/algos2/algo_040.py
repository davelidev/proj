from AlgorithmImports import *


class Algo040(QCAlgorithm):
    """Mega-7 EW + 20-day Slope of QQQ SMA50 Regime Cash Gate.

    Track SMA50 of QQQ in a 21-deep rolling window. Slope = SMA50_today
    - SMA50_20d_ago. If slope > 0: hold Mega-7 EW; else: cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        basket = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.basket_symbols = []
        for t in basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.basket_symbols.append(eq.Symbol)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma50 = self.SMA(self.qqq, 50, Resolution.Daily)
        self.sma_window = RollingWindow[float](21)
        self.sma50.Updated += self._on_sma_updated

        self.regime_in = None
        self.SetWarmUp(80, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 30),
            self.Rebalance,
        )

    def _on_sma_updated(self, sender, updated):
        if self.sma50.IsReady:
            self.sma_window.Add(float(updated.Value))

    def Rebalance(self):
        if self.IsWarmingUp:
            return
        if not self.sma_window.IsReady:
            return

        slope = self.sma_window[0] - self.sma_window[20]
        new_regime = slope > 0.0

        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self.basket_symbols)
            for sym in self.basket_symbols:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
