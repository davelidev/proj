from AlgorithmImports import *


class Algo027(QCAlgorithm):
    """#27 — 5 most mkt cap by 6mo momentum, monthly."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Coarse, self.Fine)
        self.SetWarmUp(160, Resolution.Daily)
        self.candidates = []
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def Coarse(self, coarse):
        sel = [c for c in coarse if c.HasFundamentalData and c.Price > 5]
        sel.sort(key=lambda c: c.DollarVolume, reverse=True)
        return [c.Symbol for c in sel[:200]]

    def Fine(self, fine):
        sel = [f for f in fine if f.MarketCap > 5e10]
        sel.sort(key=lambda f: f.MarketCap, reverse=True)
        # Take the top 30 largest, then we'll rank by momentum
        self.candidates = [f.Symbol for f in sel[:30]]
        return self.candidates

    def Rebalance(self):
        if self.IsWarmingUp or not self.candidates: return
        history = self.History(self.candidates, 130, Resolution.Daily)
        if history.empty: return
        moms = {}
        for sym in self.candidates:
            try:
                if sym not in history.index.get_level_values(0): continue
                closes = history.loc[sym]['close']
                if len(closes) < 130: continue
                moms[sym] = (closes.iloc[-1] / closes.iloc[0]) - 1
            except Exception: continue
        if not moms: return
        ranked = sorted(moms.items(), key=lambda x: x[1], reverse=True)
        top5 = [s for s, _ in ranked[:5]]
        if not top5: return
        w = 1.0 / len(top5)
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in top5:
                self.Liquidate(sym)
        for sym in top5:
            self.SetHoldings(sym, w)
