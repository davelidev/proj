from AlgorithmImports import *
import numpy as np


class Algo090(QCAlgorithm):
    """#090 — 4-tier vol-graded allocation: TQQQ, TQQQ+basket, basket, cash."""
    LOOKBACK = 63; TOP_N = 7
    T1 = 0.40  # vol < T1: 100% TQQQ
    T2 = 0.55  # vol < T2: 50% TQQQ + 50% basket
    T3 = 0.75  # vol < T3: 100% basket; else cash

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket = []; self.regime = "out"; self.month_seen = -1; self.weights = {}
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.basket = [f.Symbol for f in elig[:self.TOP_N]]
        return self.basket

    def _vol(self):
        h = self.History(self.tqqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return None
        c = h['close'].values; r = np.diff(np.log(c))
        return float(np.std(r) * np.sqrt(252))

    def _w(self):
        if not self.basket: return {}
        h = self.History(self.basket, self.LOOKBACK + 1, Resolution.Daily)
        if h.empty: return {}
        rets = {}
        for s in self.basket:
            try:
                if s not in h.index.get_level_values(0): continue
                c = h.loc[s]['close']
                if len(c) < self.LOOKBACK + 1: continue
                rets[s] = max(0.0, c.iloc[-1] / c.iloc[0] - 1.0)
            except: continue
        t = sum(rets.values())
        if t <= 0: return {s: 1.0 / len(self.basket) for s in self.basket}
        return {s: r / t for s, r in rets.items()}

    def _liq(self):
        for s in list(self.Portfolio.Keys):
            if self.Portfolio[s].Invested: self.Liquidate(s)

    def _set_tier(self, tier):
        self._liq()
        if tier == "tqqq":
            self.SetHoldings(self.tqqq, 1.0)
        elif tier == "mixed":
            self.weights = self._w(); self.month_seen = self.Time.month
            self.SetHoldings(self.tqqq, 0.50)
            for s, w in self.weights.items():
                if w > 0: self.SetHoldings(s, w * 0.50)
        elif tier == "basket":
            self.weights = self._w(); self.month_seen = self.Time.month
            for s, w in self.weights.items():
                if w > 0: self.SetHoldings(s, w)

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return
        if v < self.T1: nr = "tqqq"
        elif v < self.T2: nr = "mixed"
        elif v < self.T3: nr = "basket"
        else: nr = "out"

        if nr != self.regime:
            self._set_tier(nr)
            self.regime = nr
            return

        if self.regime in ("mixed", "basket") and self.Time.month != self.month_seen:
            self._set_tier(nr)
