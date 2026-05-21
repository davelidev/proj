from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TechDipBuySub(BaseSubAlgo):
    """Top-5 tech by market cap; RSI(2) < 30 & price > SMA(50) entry Mon only; 15% stop or 252-day high exit."""
    HAS_UNIVERSE = True
    SLOT_W = 0.20

    def initialize(self):
        self._anchor = self.algo.AddEquity("QQQ", Resolution.Daily).Symbol
        self._rsi   = {}
        self._max   = {}
        self._sma50 = {}

    def universe_selection(self, fundamental):
        tech = [
            f for f in fundamental
            if f.HasFundamentalData
            and f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology
        ]
        return [f.Symbol for f in sorted(tech, key=lambda f: f.MarketCap)[-5:]]

    def on_securities_changed(self, changes):
        universe_syms = self.universe_groups.get(self.id, set())
        for sec in changes.AddedSecurities:
            sym = sec.Symbol
            if sym != self._anchor and sym in universe_syms:
                self._rsi[sym]   = self.algo.RSI(sym, 2)
                self._max[sym]   = self.algo.MAX(sym, 252)
                self._sma50[sym] = self.algo.SMA(sym, 50)
        for sec in changes.RemovedSecurities:
            sym = sec.Symbol
            for d in (self._rsi, self._max, self._sma50):
                d.pop(sym, None)
            if sym in self.targets:
                del self.targets[sym]
                self.algo.Liquidate(sym)

    def update_targets(self):
        if self.algo.Time.weekday() != 0:  # Monday only
            return False
        prev = dict(self.targets)

        # Exits
        for sym in list(self.targets):
            if sym not in self._max or not self._max[sym].IsReady: continue
            price = self.algo.Securities[sym].Price
            avg   = self.algo.Portfolio[sym].AveragePrice
            if price <= avg * 0.85 or price >= self._max[sym].Current.Value:
                del self.targets[sym]

        # Drift-lock: update held position weights to current portfolio weight
        total = self.algo.Portfolio.TotalPortfolioValue
        if total > 0:
            for sym in list(self.targets):
                self.targets[sym] = self.algo.Portfolio[sym].HoldingsValue / total

        # Entries
        invested_w = sum(self.targets.values())
        budget     = max(0.0, 1.0 - invested_w)
        universe_syms = self.universe_groups.get(self.id, set())
        for sym in universe_syms:
            if sym == self._anchor or sym in self.targets or budget < 0.005: continue
            if sym not in self._rsi or not self._rsi[sym].IsReady: continue
            if not self._max[sym].IsReady or not self._sma50[sym].IsReady: continue
            price = self.algo.Securities[sym].Price
            if self._rsi[sym].Current.Value < 30 and price > self._sma50[sym].Current.Value:
                entry_w = min(self.SLOT_W, budget)
                self.targets[sym] = entry_w
                budget -= entry_w

        return self.targets != prev


TechDipBuyAlgo = _make_standalone(TechDipBuySub)
