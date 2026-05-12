from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MktCapIBSRegimeSub(BaseSubAlgo):
    """#064 — 5 most mkt cap + IBS regime mix."""

    HAS_UNIVERSE = True

    def initialize(self):
        self.qqq = self.algo.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.algo.SMA(self.qqq, 200, Resolution.Daily)

    def universe_selection(self, fundamental):
        elig = [f for f in fundamental if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        return [f.Symbol for f in elig[:5]]

    def on_securities_changed(self, changes):
        for sec in changes.RemovedSecurities:
            self.targets.pop(sec.Symbol, None)

    def update_targets(self):
        if not self.sma.IsReady: return False

        symbols = self.universe_groups.get(self.id, set())
        if not symbols: return False

        prev = dict(self.targets)
        in_trend = self.algo.Securities[self.qqq].Price > self.sma.Current.Value

        if in_trend:
            w = 1.0 / len(symbols)
            for sym in symbols:
                self.targets[sym] = w
            for sym in list(self.targets):
                if sym not in symbols:
                    del self.targets[sym]
        else:
            targets = []
            for s in symbols:
                bar = self.algo.Securities[s]
                h, l, c = bar.High, bar.Low, bar.Close
                if h <= l: continue
                ibs = (c - l) / (h - l)
                if ibs < 0.2:
                    targets.append(s)
            if targets:
                w = 1.0 / len(targets)
                for s in targets:
                    self.targets[s] = w
            for sym in list(self.targets):
                if sym not in targets:
                    del self.targets[sym]

        return self.targets != prev


MktCapIBSRegimeAlgo = _make_standalone(MktCapIBSRegimeSub)
