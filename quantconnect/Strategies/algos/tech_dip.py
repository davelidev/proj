from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TechDipBuySub(BaseSubAlgo):
    HAS_UNIVERSE = True

    def initialize(self):
        self.algo.Settings.AutomaticIndicatorWarmUp = True
        self.algo.Settings.SeedInitialPrices = True

    def universe_selection(self, fundamental):
        filtered = [
            f for f in fundamental
            if f.HasFundamentalData and
               f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology
        ]
        return [f.Symbol for f in sorted(filtered, key=lambda f: f.MarketCap)[-5:]]

    def on_securities_changed(self, changes):
        tech = self.universe_groups.get("TechDipBuySub", set())
        for sec in changes.AddedSecurities:
            if sec.Symbol not in tech: continue
            sec.rsi   = self.algo.RSI(sec.Symbol, 2)
            sec.max   = self.algo.MAX(sec.Symbol, 252)
            sec.sma50 = self.algo.SMA(sec.Symbol, 50)
        for sec in changes.RemovedSecurities:
            self.targets.pop(sec.Symbol, None)
            self.algo.Liquidate(sec.Symbol)

    def update_targets(self):
        tech = self.universe_groups.get("TechDipBuySub", set())
        if not tech or self.algo.Time.weekday() != 0: return False

        total_value = self.algo.Portfolio.TotalPortfolioValue
        w = 1.0 / 5
        prev = dict(self.targets)

        # Step 1: process exits; drift-lock survivors so base never trims winners
        for s in tech:
            sec = self.algo.Securities[s]
            if not sec.Invested: continue
            if not (hasattr(sec, "max") and sec.max.IsReady and sec.sma50.IsReady): continue
            if sec.Price <= sec.Holdings.AveragePrice * 0.85 or sec.Price >= sec.max.Current.Value:
                self.targets.pop(s, None)
            else:
                self.targets[s] = sec.Holdings.HoldingsValue / total_value

        # Step 2: new entries up to remaining cash budget so scale never drops below 1
        budget = max(0.0, 1.0 - sum(self.targets.values()))
        for s in tech:
            sec = self.algo.Securities[s]
            if sec.Invested or s in self.targets: continue
            if not (hasattr(sec, "max") and sec.max.IsReady and sec.sma50.IsReady): continue
            if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value and budget >= 0.005:
                entry_w = min(w, budget)
                self.targets[s] = entry_w
                budget -= entry_w

        return self.targets != prev


TechDipBuyAlgo = _make_standalone(TechDipBuySub)
