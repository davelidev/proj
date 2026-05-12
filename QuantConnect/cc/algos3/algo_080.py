from AlgorithmImports import *
import numpy as np


class Algo080(QCAlgorithm):
    """#080 — #075 with adaptive vol thresholds (252d-rolling-median based).
    calm = current vol < 0.7 × 252d-median; panic = vol > 2.0 × median.
    Else basket regime.
    """
    LOOKBACK = 63; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(280, Resolution.Daily)
        self.basket = []; self.regime = "out"; self.month_seen = -1; self.weights = {}
        self.vol_window = RollingWindow[float](253)
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

    def _liquidate_all(self):
        for s in list(self.Portfolio.Keys):
            if self.Portfolio[s].Invested: self.Liquidate(s)

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return
        self.vol_window.Add(v)
        if not self.vol_window.IsReady:
            calm_thr = 0.55; panic_thr = 0.85
        else:
            vals = sorted([self.vol_window[i] for i in range(self.vol_window.Count)])
            median = vals[len(vals) // 2]
            calm_thr = 0.7 * median
            panic_thr = 2.0 * median

        if v >= panic_thr: new_regime = "out"
        elif v < calm_thr: new_regime = "tqqq"
        else: new_regime = "basket"

        if new_regime != self.regime:
            self._liquidate_all()
            if new_regime == "tqqq":
                self.SetHoldings(self.tqqq, 1.0)
            elif new_regime == "basket":
                self.weights = self._w(); self.month_seen = self.Time.month
                for s, w in self.weights.items():
                    if w > 0: self.SetHoldings(s, w)
            self.regime = new_regime
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
