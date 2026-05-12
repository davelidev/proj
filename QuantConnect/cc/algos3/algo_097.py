from AlgorithmImports import *
import numpy as np


class Algo097(QCAlgorithm):
    """#097 — Regime switch using BOTH 20d AND 60d vol. Both must agree to flip regime."""
    LOOKBACK = 63; CALM_VOL = 0.55; PANIC_VOL = 0.85; TOP_N = 7

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

    def _vols(self):
        h = self.History(self.tqqq, 61, Resolution.Daily)
        if h.empty or len(h) < 61: return None, None
        c = h['close'].values; r = np.diff(np.log(c))
        v20 = float(np.std(r[-20:]) * np.sqrt(252))
        v60 = float(np.std(r) * np.sqrt(252))
        return v20, v60

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

    def _classify(self, v):
        if v >= self.PANIC_VOL: return "out"
        elif v < self.CALM_VOL: return "tqqq"
        else: return "basket"

    def _liq(self):
        for s in list(self.Portfolio.Keys):
            if self.Portfolio[s].Invested: self.Liquidate(s)

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v20, v60 = self._vols()
        if v20 is None: return
        c20 = self._classify(v20)
        c60 = self._classify(v60)
        # Only flip if both agree, else stay in current regime
        if c20 == c60: nr = c20
        else: nr = self.regime  # no flip on disagreement

        if nr != self.regime:
            self._liq()
            if nr == "tqqq": self.SetHoldings(self.tqqq, 1.0)
            elif nr == "basket":
                self.weights = self._w(); self.month_seen = self.Time.month
                for s, w in self.weights.items():
                    if w > 0: self.SetHoldings(s, w)
            self.regime = nr
            return

        if self.regime == "basket" and self.Time.month != self.month_seen:
            self.weights = self._w(); self.month_seen = self.Time.month
            target_set = set(self.weights.keys())
            for s in list(self.Portfolio.Keys):
                if s != self.tqqq and self.Portfolio[s].Invested and s not in target_set:
                    self.Liquidate(s)
            for s, w in self.weights.items():
                cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                if abs(w - cur) > 0.03 and w > 0: self.SetHoldings(s, w)
