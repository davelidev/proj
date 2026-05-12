from AlgorithmImports import *


class Algo020(QCAlgorithm):
    """#20 — Top 5 by 12-1 momentum from S&P 500 universe, monthly rebalance, equal weight, no leverage."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Coarse, self.Fine)
        self.SetWarmUp(280, Resolution.Daily)
        self.candidates = []
        self.history_cache = {}
        self.Schedule.On(self.DateRules.MonthStart(),
                         self.TimeRules.At(10, 0),
                         self.Rebalance)

    def Coarse(self, coarse):
        # top 200 by dollar volume
        sel = [c for c in coarse if c.HasFundamentalData and c.Price > 5]
        sel.sort(key=lambda c: c.DollarVolume, reverse=True)
        return [c.Symbol for c in sel[:200]]

    def Fine(self, fine):
        sel = [f for f in fine if f.MarketCap > 1e10]
        sel.sort(key=lambda f: f.MarketCap, reverse=True)
        self.candidates = [f.Symbol for f in sel[:100]]
        return self.candidates

    def Rebalance(self):
        if self.IsWarmingUp: return
        if not self.candidates: return
        # Compute 12-1 momentum (252-21 day return)
        history = self.History(self.candidates, 252, Resolution.Daily)
        if history.empty: return
        moms = {}
        for sym in self.candidates:
            try:
                if sym not in history.index.get_level_values(0): continue
                closes = history.loc[sym]['close']
                if len(closes) < 252: continue
                p_252 = closes.iloc[0]
                p_21  = closes.iloc[-21]
                if p_252 > 0:
                    moms[sym] = (p_21 / p_252) - 1
            except Exception:
                continue
        if not moms: return
        ranked = sorted(moms.items(), key=lambda x: x[1], reverse=True)
        top5 = [s for s, _ in ranked[:5]]
        if not top5: return

        weight = 1.0 / len(top5)
        for sym in list(self.Portfolio.Keys):
            if self.Portfolio[sym].Invested and sym not in top5:
                self.Liquidate(sym)
        for sym in top5:
            self.SetHoldings(sym, weight)
