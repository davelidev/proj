from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class GiantSniperSub(BaseSubAlgo):
    """Top-5 mega-caps; QQQ SMA(200) bear shield; RSI(2) < 20 entry; RSI(2) > 70 exit."""
    HAS_UNIVERSE = True

    def initialize(self):
        self.qqq    = self.algo.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma200 = self.algo.SMA(self.qqq, 200)
        self._rsi   = {}

    def universe_selection(self, fundamental):
        top5 = sorted(
            [f for f in fundamental if f.MarketCap > 0],
            key=lambda f: f.MarketCap, reverse=True,
        )[:5]
        return [f.Symbol for f in top5]

    def on_securities_changed(self, changes):
        universe_syms = self.universe_groups.get(self.id, set())
        for sec in changes.AddedSecurities:
            sym = sec.Symbol
            if sym != self.qqq and sym in universe_syms:
                self._rsi[sym] = self.algo.RSI(sym, 2, MovingAverageType.Wilders)
        for sec in changes.RemovedSecurities:
            sym = sec.Symbol
            self._rsi.pop(sym, None)
            if sym in self.targets:
                del self.targets[sym]
                self.algo.Liquidate(sym)

    def update_targets(self):
        if not self.sma200.IsReady:
            return False
        prev = dict(self.targets)
        is_bull = self.algo.Securities[self.qqq].Price > self.sma200.Current.Value

        if not is_bull:
            self.targets = {}
        else:
            # Exit: RSI(2) > 70
            for sym in list(self.targets):
                if sym in self._rsi and self._rsi[sym].IsReady:
                    if self._rsi[sym].Current.Value > 70:
                        del self.targets[sym]

            # Entry: RSI(2) < 20, not yet held
            universe_syms = self.universe_groups.get(self.id, set())
            for sym in universe_syms:
                if sym == self.qqq or sym in self.targets: continue
                if sym not in self._rsi or not self._rsi[sym].IsReady: continue
                if self._rsi[sym].Current.Value < 20:
                    self.targets[sym] = 0.0  # weight set below

            # Equal-weight all held positions
            if self.targets:
                w = 1.0 / len(self.targets)
                for sym in self.targets:
                    self.targets[sym] = w

        return self.targets != prev


GiantSniperAlgo = _make_standalone(GiantSniperSub)
