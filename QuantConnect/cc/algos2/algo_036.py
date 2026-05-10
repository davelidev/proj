from AlgorithmImports import *


class Algo036(QCAlgorithm):
    """Top-5 Mega-Cap (live universe, monthly) + QQQ Drawdown-from-Peak Cash Gate.

    Live universe: top-5 by market cap (fundamental selection, monthly cadence).
    Signal: QQQ drawdown from 252-day max. Hold top-5 EW if drawdown > -10%
    (within 10% of peak); otherwise cash.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelection, self.FineSelection)

        self._last_universe_month = -1
        self._top5 = []  # symbols selected by latest fine selection

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.qqq_max = self.MAX(self.qqq, 252, Resolution.Daily)

        self.regime_in = None
        self.SetWarmUp(260, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.EveryDay("QQQ"),
            self.TimeRules.AfterMarketOpen("QQQ", 30),
            self.Rebalance,
        )

    def CoarseSelection(self, coarse):
        # Refresh once per month
        m = self.Time.month
        if m == self._last_universe_month:
            return Universe.Unchanged
        self._last_universe_month = m

        filtered = [c for c in coarse
                    if c.HasFundamentalData and c.Price > 5 and c.DollarVolume > 1e7]
        filtered.sort(key=lambda c: c.DollarVolume, reverse=True)
        return [c.Symbol for c in filtered[:200]]

    def FineSelection(self, fine):
        valid = [f for f in fine
                 if f.MarketCap is not None and f.MarketCap > 0]
        valid.sort(key=lambda f: f.MarketCap, reverse=True)
        top = valid[:5]
        self._top5 = [f.Symbol for f in top]
        return self._top5

    def Rebalance(self):
        if self.IsWarmingUp or not self.qqq_max.IsReady:
            return
        if not self._top5:
            return

        price = self.Securities[self.qqq].Price
        peak = self.qqq_max.Current.Value
        if peak <= 0:
            return
        dd = price / peak - 1.0  # negative or zero

        new_regime = dd > -0.10

        # Liquidate names that fell out of top-5
        held = [kvp.Key for kvp in self.Portfolio if kvp.Value.Invested]
        for sym in held:
            if sym not in self._top5:
                self.Liquidate(sym)

        if new_regime:
            w = 1.0 / len(self._top5)
            for sym in self._top5:
                self.SetHoldings(sym, w)
            self.regime_in = True
        else:
            self.Liquidate()
            self.regime_in = False
