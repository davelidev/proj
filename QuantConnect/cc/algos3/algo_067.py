from AlgorithmImports import *
import numpy as np


class Algo067(QCAlgorithm):
    """#067 — Top-7 cap-weighted (by mkt cap from fundamental data) + TQQQ vol gate."""
    VOL_THRESH = 0.60; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket_data = []  # list of (Symbol, mktcap)
        self.in_market = False; self.month_seen = -1
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.basket_data = [(f.Symbol, float(f.MarketCap)) for f in elig[:self.TOP_N]]
        return [s for s, _ in self.basket_data]

    def _vol(self):
        h = self.History(self.tqqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return None
        c = h['close'].values; r = np.diff(np.log(c))
        return float(np.std(r) * np.sqrt(252))

    def _w(self):
        if not self.basket_data: return {}
        total = sum(mc for _, mc in self.basket_data)
        if total <= 0: return {}
        return {s: mc / total for s, mc in self.basket_data}

    def R(self):
        if self.IsWarmingUp or not self.basket_data: return
        v = self._vol()
        if v is None: return
        on = v < self.VOL_THRESH
        if on:
            weights = self._w()
            target_set = set(weights.keys())
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested and s != self.tqqq and s not in target_set: self.Liquidate(s)
            for s, w in weights.items():
                cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                if not self.in_market or abs(w - cur) > 0.05:
                    if w > 0: self.SetHoldings(s, w)
            self.in_market = True
        else:
            if self.in_market:
                for s in list(self.Portfolio.Keys):
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
