from AlgorithmImports import *
import numpy as np


class Algo054(QCAlgorithm):
    """#054 — Mega-7 top-3 by 3mo momentum (zero-out bottom 4) + TQQQ vol gate."""
    LOOKBACK = 63
    VOL_THRESH = 0.60
    MEGA = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.syms = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.MEGA]
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
        h = self.History(self.syms, self.LOOKBACK + 1, Resolution.Daily)
        if h.empty: return {}
        rets = {}
        for s in self.syms:
            try:
                if s not in h.index.get_level_values(0): continue
                c = h.loc[s]['close']
                if len(c) < self.LOOKBACK + 1: continue
                rets[s] = c.iloc[-1] / c.iloc[0] - 1.0
            except Exception: continue
        if not rets: return {}
        ranked = sorted(rets.items(), key=lambda kv: kv[1], reverse=True)[:3]
        positive = [(s, max(0.0, r)) for s, r in ranked]
        total = sum(r for _, r in positive)
        if total <= 0:
            return {s: 1.0 / 3 for s, _ in ranked}
        return {s: r / total for s, r in positive if r > 0}

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
            if self.weights:
                target_set = set(self.weights.keys())
                for s in self.syms:
                    if self.Portfolio[s].Invested and s not in target_set:
                        self.Liquidate(s)
                for s, w in self.weights.items():
                    cur = self.Portfolio[s].HoldingsValue / self.Portfolio.TotalPortfolioValue if self.Portfolio.TotalPortfolioValue > 0 else 0
                    if not self.in_market or abs(w - cur) > 0.05:
                        self.SetHoldings(s, w)
                self.in_market = True
        else:
            if self.in_market:
                for s in self.syms:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
