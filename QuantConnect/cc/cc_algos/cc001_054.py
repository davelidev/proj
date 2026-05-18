from AlgorithmImports import *
import numpy as np


class Algo060(QCAlgorithm):
    """#060 — Mega-7 momo-weighted (3mo) + TQQQ vol-gate + sleeve mix.
    When vol calm: 80% Mega-7 momo + 20% TQQQ.
    When vol regime breaks: 100% cash.
    """
    LOOKBACK = 63
    VOL_THRESH = 0.60
    BASKET_W = 0.80
    TQQQ_W = 0.20

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.SetWarmUp(150, Resolution.Daily)
        self.in_market = False
        self.month_seen = -1
        self.weights = {}
        self.Schedule.On(self.DateRules.EveryDay(self.tqqq),
                         self.TimeRules.AfterMarketOpen(self.tqqq, 30), self.R)

    def _vol(self):
        h = self.History(self.tqqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return None
        c = h['close'].values
        r = np.diff(np.log(c))
        return float(np.std(r) * np.sqrt(252))

    def _compute_weights(self):
        h = self.History(self._universe, self.LOOKBACK + 1, Resolution.Daily)
        if h.empty: return {}
        rets = {}
        for s in self._universe:
            try:
                if s not in h.index.get_level_values(0): continue
                c = h.loc[s]['close']
                if len(c) < self.LOOKBACK + 1: continue
                rets[s] = max(0.0, c.iloc[-1] / c.iloc[0] - 1.0)
            except Exception: continue
        total = sum(rets.values())
        if total <= 0:
            return {s: 1.0 / len(self._universe) for s in self._universe}
        return {s: r / total for s, r in rets.items()}


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def R(self):
        if self.IsWarmingUp: return
        v = self._vol()
        if v is None: return
        gate_on = v < self.VOL_THRESH

        if gate_on:
            month = self.Time.month
            if month != self.month_seen or not self.in_market:
                self.weights = self._compute_weights()
                self.month_seen = month
            # Apply Mega-7 sleeve at 80%
            for s in self._universe:
                w = self.weights.get(s, 0.0) * self.BASKET_W
                cur = self.Portfolio[s].HoldingsValue / self.Portfolio.TotalPortfolioValue if self.Portfolio.TotalPortfolioValue > 0 else 0
                if not self.in_market or abs(w - cur) > 0.03:
                    self.SetHoldings(s, w)
            # TQQQ sleeve at 20%
            cur_t = self.Portfolio[self.tqqq].HoldingsValue / self.Portfolio.TotalPortfolioValue if self.Portfolio.TotalPortfolioValue > 0 else 0
            if not self.in_market or abs(self.TQQQ_W - cur_t) > 0.03:
                self.SetHoldings(self.tqqq, self.TQQQ_W)
            self.in_market = True
        else:
            if self.in_market:
                for s in self._universe:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                if self.Portfolio[self.tqqq].Invested: self.Liquidate(self.tqqq)
                self.in_market = False
