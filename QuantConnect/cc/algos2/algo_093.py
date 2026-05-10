from AlgorithmImports import *
import numpy as np


class Algo093(QCAlgorithm):
    """#093 — Regime switch with cap-weighted basket (live mkt-cap weights from fundamentals)."""
    CALM_VOL = 0.55; PANIC_VOL = 0.85; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket_data = []  # (Symbol, mktcap)
        self.regime = "out"; self.month_seen = -1
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

    def _liq(self):
        for s in list(self.Portfolio.Keys):
            if self.Portfolio[s].Invested: self.Liquidate(s)

    def R(self):
        if self.IsWarmingUp or not self.basket_data: return
        v = self._vol()
        if v is None: return
        if v >= self.PANIC_VOL: nr = "out"
        elif v < self.CALM_VOL: nr = "tqqq"
        else: nr = "basket"

        if nr != self.regime:
            self._liq()
            if nr == "tqqq": self.SetHoldings(self.tqqq, 1.0)
            elif nr == "basket":
                ws = self._w(); self.month_seen = self.Time.month
                for s, w in ws.items():
                    if w > 0: self.SetHoldings(s, w)
            self.regime = nr
            return

        if self.regime == "basket" and self.Time.month != self.month_seen:
            ws = self._w(); self.month_seen = self.Time.month
            target_set = set(ws.keys())
            for s in list(self.Portfolio.Keys):
                if s != self.tqqq and self.Portfolio[s].Invested and s not in target_set:
                    self.Liquidate(s)
            for s, w in ws.items():
                cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
                if abs(w - cur) > 0.03 and w > 0: self.SetHoldings(s, w)
