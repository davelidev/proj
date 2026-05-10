from AlgorithmImports import *
import numpy as np


class Algo095(QCAlgorithm):
    """#095 — TQQQ regime + top-7 EW basket (no momentum weighting). Simpler basket variant of #075."""
    CALM_VOL = 0.55; PANIC_VOL = 0.85; TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket = []; self.regime = "out"
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

    def _liq(self):
        for s in list(self.Portfolio.Keys):
            if self.Portfolio[s].Invested: self.Liquidate(s)

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return
        if v >= self.PANIC_VOL: nr = "out"
        elif v < self.CALM_VOL: nr = "tqqq"
        else: nr = "basket"

        if nr != self.regime:
            self._liq()
            if nr == "tqqq":
                self.SetHoldings(self.tqqq, 1.0)
            elif nr == "basket":
                w = 1.0 / len(self.basket)
                for s in self.basket: self.SetHoldings(s, w)
            self.regime = nr
