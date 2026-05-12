from AlgorithmImports import *
import numpy as np


class Algo079(QCAlgorithm):
    """#079 — TQQQ size scales linearly by inverse vol; rest in dyn top-7 EW.
    target_tqqq = clip((0.80 - vol) / 0.40, 0.0, 1.0)
    rest = 1.0 - target_tqqq, distributed equal-weight to top-7 dyn basket.
    """
    TOP_N = 7

    def Initialize(self):
        self.SetStartDate(2014, 1, 1); self.SetEndDate(2025, 12, 31); self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.AddUniverse(self.Sel); self.SetWarmUp(150, Resolution.Daily)
        self.basket = []
        self.last_target = None
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

    def R(self):
        if self.IsWarmingUp or not self.basket: return
        v = self._vol()
        if v is None: return

        # tqqq weight: 1.0 at vol=0.40, 0.0 at vol=0.80, linear between
        tqqq_w = max(0.0, min(1.0, (0.80 - v) / 0.40))
        basket_w = 1.0 - tqqq_w
        per_name = basket_w / len(self.basket) if self.basket else 0

        # Only trade if change is meaningful
        if self.last_target is not None and abs(self.last_target - tqqq_w) < 0.05:
            return

        target_set = set(self.basket)
        for s in list(self.Portfolio.Keys):
            if s != self.tqqq and self.Portfolio[s].Invested and s not in target_set:
                self.Liquidate(s)

        for s in self.basket:
            cur = self.Portfolio[s].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
            if abs(per_name - cur) > 0.03:
                self.SetHoldings(s, per_name)
        cur_t = self.Portfolio[self.tqqq].HoldingsValue / max(1e-9, self.Portfolio.TotalPortfolioValue)
        if abs(tqqq_w - cur_t) > 0.03:
            self.SetHoldings(self.tqqq, tqqq_w)
        self.last_target = tqqq_w
