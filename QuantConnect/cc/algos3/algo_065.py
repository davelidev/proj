from AlgorithmImports import *
import numpy as np


class Algo065(QCAlgorithm):
    """#065 — Top-7 mkt-cap momo (3mo) + TQQQ dual vol+ATR gate (replicate #058)."""
    LOOKBACK = 63; VOL_THRESH = 0.60; ATR_HARD = 0.06; ATR_REENTRY = 0.045; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
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
        if self.IsWarmingUp or not self.atr.IsReady or not self.basket: return
        v = self._vol()
        if v is None: return
        tqqq_px = self.Securities[self.tqqq].Price
        atr_pct = self.atr.Current.Value / tqqq_px if tqqq_px > 0 else 0

        if self.in_market:
            if v >= self.VOL_THRESH or atr_pct > self.ATR_HARD:
                for s in list(self.Portfolio.Keys):
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
                return
        else:
            if v < self.VOL_THRESH and atr_pct < self.ATR_REENTRY:
                self.weights = self._w(); self.month_seen = self.Time.month
                target_set = set(self.weights.keys())
                for s in list(self.Portfolio.Keys):
                    if self.Portfolio[s].Invested and s != self.tqqq and s not in target_set: self.Liquidate(s)
                for s, w in self.weights.items():
                    if w > 0: self.SetHoldings(s, w)
                self.in_market = True
                return

        if self.in_market and self.Time.month != self.month_seen:
            self.weights = self._w(); self.month_seen = self.Time.month
            target_set = set(self.weights.keys())
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested and s != self.tqqq and s not in target_set: self.Liquidate(s)
            for s, w in self.weights.items():
                cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                if abs(w - cur) > 0.05: self.SetHoldings(s, w)
