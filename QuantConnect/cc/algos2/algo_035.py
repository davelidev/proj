from AlgorithmImports import *


class Algo035(QCAlgorithm):
    """7 Leveraged Sector ETFs EW + Cross-Sector Breadth Gate.

    Hold all 7 EW when at least 5 of 7 ETFs have positive 50-day return.
    Otherwise cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        basket = ["TQQQ", "TECL", "SOXL", "FAS", "CURE", "DPST", "TNA"]
        self.basket_symbols = []
        for t in basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.basket_symbols.append(eq.Symbol)

        self.regime_in = None
        self.SetWarmUp(60, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay(self.basket_symbols[0]),
            self.TimeRules.AfterMarketOpen(self.basket_symbols[0], 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        positives = 0
        total = 0
        for sym in self.basket_symbols:
            hist = self.History(sym, 51, Resolution.Daily)
            if hist is None or hist.empty:
                continue
            try:
                closes = hist["close"].values
            except Exception:
                continue
            if len(closes) < 51:
                continue
            ret = closes[-1] / closes[0] - 1.0
            total += 1
            if ret > 0:
                positives += 1

        if total == 0:
            return
        new_regime = positives >= 5

        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self.basket_symbols)
            for sym in self.basket_symbols:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
