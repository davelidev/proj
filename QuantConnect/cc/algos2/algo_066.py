from AlgorithmImports import *
import numpy as np


class Algo066(QCAlgorithm):
    """#066 — Top-7 momo + TQQQ vol-50% (tighter)."""
    LOOKBACK = 63; VOL_THRESH = 0.50; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket = []; self.in_market = False; self.month_seen = -1; self.weights = {}
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

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return
        on = v < self.VOL_THRESH
        if on:
            if self.Time.month != self.month_seen or not self.in_market:
                self.weights = self._w(); self.month_seen = self.Time.month
            target_set = set(self.weights.keys())
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested and s != self.tqqq and s not in target_set: self.Liquidate(s)
            for s, w in self.weights.items():
                cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                if not self.in_market or abs(w - cur) > 0.05:
                    if w > 0: self.SetHoldings(s, w)
            self.in_market = True
        else:
            if self.in_market:
                for s in list(self.Portfolio.Keys):
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
