from AlgorithmImports import *


class Algo031(QCAlgorithm):
    """Mega-7 EW + Breadth-of-Sectors Cash Gate.

    Hold Mega-7 equal-weight when at least 50% of 11 SPDR sector ETFs have
    positive 21-day returns; otherwise go to cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)


        sectors = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLI",
                   "XLP", "XLU", "XLB", "XLRE", "XLC"]
        self.sector_symbols = []
        for t in sectors:
            eq = self.AddEquity(t, Resolution.Daily)
            self.sector_symbols.append(eq.Symbol)

        self.regime_in = None  # None to force first decision
        self._universe = []    # init before first rebalance
        self.SetWarmUp(30, Resolution.Daily)
        self.AddUniverse(self._Sel)

        self.Schedule.On(
            self.DateRules.EveryDay("XLK"),
            self.TimeRules.AfterMarketOpen("XLK", 30),
            self.Rebalance,
        )


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        positives = 0
        total = 0
        for sym in self.sector_symbols:
            hist = self.History(sym, 22, Resolution.Daily)
            if hist is None or hist.empty:
                continue
            try:
                closes = hist["close"].values
            except Exception:
                continue
            if len(closes) < 22:
                continue
            ret = closes[-1] / closes[0] - 1.0
            total += 1
            if ret > 0:
                positives += 1

        if total == 0:
            return
        breadth = positives / total
        new_regime = breadth >= 0.5

        if new_regime == self.regime_in:
            return
        self.regime_in = new_regime

        if new_regime and self._universe:
            w = 1.0 / len(self._universe)
            for sym in self._universe:
                self.SetHoldings(sym, w)
        else:
            self.Liquidate()
