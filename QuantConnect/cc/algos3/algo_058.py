from AlgorithmImports import *
import numpy as np


class Algo058(QCAlgorithm):
    """#058 — Mega-7 momo-weighted (3mo) + dual TQQQ-vol gate (vol AND ATR escalation)."""
    LOOKBACK = 63
    VOL_THRESH = 0.60
    ATR_PCT_HARD_EXIT = 0.06
    ATR_PCT_REENTRY = 0.045

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.atr = self.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
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
        if self.IsWarmingUp or not self.atr.IsReady: return
        v = self._vol()
        if v is None: return
        tqqq_px = self.Securities[self.tqqq].Price
        atr_pct = self.atr.Current.Value / tqqq_px if tqqq_px > 0 else 0

        if self.in_market:
            # Hard exit if ATR escalates
            if v >= self.VOL_THRESH or atr_pct > self.ATR_PCT_HARD_EXIT:
                for s in self._universe:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
                return
        else:
            # Re-enter only when vol is calm AND ATR has settled
            if v < self.VOL_THRESH and atr_pct < self.ATR_PCT_REENTRY:
                self.weights = self._compute_weights()
                self.month_seen = self.Time.month
                for s in self._universe:
                    w = self.weights.get(s, 0.0)
                    if w > 0: self.SetHoldings(s, w)
                self.in_market = True
                return

        # Monthly weight rebalance while in market
        if self.in_market and self.Time.month != self.month_seen:
            self.weights = self._compute_weights()
            self.month_seen = self.Time.month
            for s in self._universe:
                w = self.weights.get(s, 0.0)
                cur = self.Portfolio[s].HoldingsValue / self.Portfolio.TotalPortfolioValue if self.Portfolio.TotalPortfolioValue > 0 else 0
                if abs(w - cur) > 0.05:
                    self.SetHoldings(s, w)
