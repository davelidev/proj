from AlgorithmImports import *


class Algo037(QCAlgorithm):
    """Leveraged-Tech Trio + XLK-vs-XLP Realized-Spread Cash Gate.

    Basket: TQQQ, TECL, SOXL (EW). Spread = XLK 20d return - XLP 20d return.
    Long basket if spread > 0; cash otherwise.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        basket = ["TQQQ", "TECL", "SOXL"]
        self.basket_symbols = []
        for t in basket:
            eq = self.AddEquity(t, Resolution.Daily)
            self.basket_symbols.append(eq.Symbol)

        self.xlk = self.AddEquity("XLK", Resolution.Daily).Symbol
        self.xlp = self.AddEquity("XLP", Resolution.Daily).Symbol

        self.regime_in = None
        self.SetWarmUp(30, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("XLK"),
            self.TimeRules.AfterMarketOpen("XLK", 30),
            self.Rebalance,
        )

    def _ret_20d(self, sym):
        hist = self.History(sym, 22, Resolution.Daily)
        if hist is None or hist.empty:
            return None
        try:
            closes = hist["close"].values
        except Exception:
            return None
        if len(closes) < 22:
            return None
        return closes[-1] / closes[0] - 1.0


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        rk = self._ret_20d(self.xlk)
        rp = self._ret_20d(self.xlp)
        if rk is None or rp is None:
            return

        spread = rk - rp
        new_regime = spread > 0.0

        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime:
            w = 1.0 / len(self.basket_symbols)
            for sym in self.basket_symbols:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
