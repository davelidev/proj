from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TechDipBuySub(BaseSubAlgo):
    HAS_UNIVERSE = True

    def initialize(self):
        self.selected_syms = []

    def universe_selection(self, fundamental):
        tech = [f for f in fundamental
                if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        top5 = sorted(tech, key=lambda x: x.MarketCap, reverse=True)[:5]
        return [x.Symbol for x in top5]

    def on_securities_changed(self, changes):
        skip = {"TQQQ", "QQQ", "SOXL", "TECL", "SPY", "BIL"}
        for sec in changes.AddedSecurities:
            if sec.Symbol.Value in skip: continue
            sec.rsi   = self.algo.RSI(sec.Symbol, 2)
            sec.max   = self.algo.MAX(sec.Symbol, 252)
            sec.sma50 = self.algo.SMA(sec.Symbol, 50)
            hist = self.algo.History(sec.Symbol, 252, Resolution.Daily)
            for bar in hist.itertuples():
                sec.rsi.Update(bar.Index[1], bar.close)
                sec.max.Update(bar.Index[1], bar.close)
                sec.sma50.Update(bar.Index[1], bar.close)
            if sec.Symbol not in self.selected_syms:
                self.selected_syms.append(sec.Symbol)
        for sec in changes.RemovedSecurities:
            if sec.Symbol in self.selected_syms:
                self.selected_syms.remove(sec.Symbol)
            if sec.Symbol in self.targets:
                del self.targets[sec.Symbol]

    def update_targets(self) -> bool:
        if self.algo.Time.weekday() != 0: return False
        if not self.selected_syms: return False
        changed = False
        w = 1.0 / len(self.selected_syms)
        for s in self.selected_syms:
            sec = self.algo.Securities[s]
            if not (hasattr(sec, "rsi") and sec.rsi.IsReady): continue
            old_w = self.targets.get(s, 0)
            if old_w == 0:
                if sec.rsi.Current.Value < 30 and sec.Price > sec.sma50.Current.Value:
                    self.targets[s] = w
                    changed = True
            else:
                avg_price = sec.Holdings.AveragePrice if sec.Invested else 0
                if (avg_price > 0 and sec.Price <= avg_price * 0.85) or sec.Price >= sec.max.Current.Value:
                    self.targets[s] = 0
                    changed = True
        return changed


TechDipBuyAlgo = _make_standalone(TechDipBuySub)
