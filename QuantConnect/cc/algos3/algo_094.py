from AlgorithmImports import *
import numpy as np


class Algo094(QCAlgorithm):
    """#094 — TQQQ + basket regime, but in TQQQ regime use 90% TQQQ + 10% top-3 of basket
    (small concentration sleeve to capture single-name outperformance even in calm regime).
    """
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

    def _vol(self):
        h = self.History(self.tqqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return None
        c = h['close'].values; r = np.diff(np.log(c))
        return float(np.std(r) * np.sqrt(252))

    def _top3_momo(self):
        if not self.basket: return []
        h = self.History(self.basket, self.LOOKBACK + 1, Resolution.Daily)
        if h.empty: return []
        rets = {}
        for s in self.basket:
            try:
                if s not in h.index.get_level_values(0): continue
                c = h.loc[s]['close']
                if len(c) < self.LOOKBACK + 1: continue
                rets[s] = c.iloc[-1] / c.iloc[0] - 1.0
            except: continue
        if not rets: return []
        return [s for s, _ in sorted(rets.items(), key=lambda kv: kv[1], reverse=True)[:3]]

    def _w_full(self):
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

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return
        if v >= self.PANIC_VOL: nr = "out"
        elif v < self.CALM_VOL: nr = "tqqq_plus"
        else: nr = "basket"

        if nr != self.regime:
            self._liq()
            if nr == "tqqq_plus":
                self.SetHoldings(self.tqqq, 0.90)
                top3 = self._top3_momo()
                if top3:
                    per = 0.10 / len(top3)
                    for s in top3: self.SetHoldings(s, per)
                self.month_seen = self.Time.month
            elif nr == "basket":
                self.weights = self._w_full(); self.month_seen = self.Time.month
                for s, w in self.weights.items():
                    if w > 0: self.SetHoldings(s, w)
            self.regime = nr
            return

        # Monthly rebalance for both basket-containing regimes
        if self.regime in ("basket", "tqqq_plus") and self.Time.month != self.month_seen:
            self.month_seen = self.Time.month
            if self.regime == "tqqq_plus":
                self._liq()
                self.SetHoldings(self.tqqq, 0.90)
                top3 = self._top3_momo()
                if top3:
                    per = 0.10 / len(top3)
                    for s in top3: self.SetHoldings(s, per)
            else:
                self.weights = self._w_full()
                target_set = set(self.weights.keys())
                for s in list(self.Portfolio.Keys):
                    if s != self.tqqq and self.Portfolio[s].Invested and s not in target_set:
                        self.Liquidate(s)
                for s, w in self.weights.items():
                    cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                    if abs(w - cur) > 0.03 and w > 0: self.SetHoldings(s, w)
