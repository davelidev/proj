from AlgorithmImports import *
import numpy as np


class Algo046(QCAlgorithm):
    """Mega-7 + QQQ 20d vol < 25% gate + monthly 3mo-momentum weighting."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)

        self.vol_threshold = 0.25
        self.in_market = False

        # Monthly momentum weights, normalized; default to EW until first computation.
        self.weights = {}

        self.Schedule.On(
            self.DateRules.MonthStart(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 20),
            self.RecomputeWeights,
        )
        self.Schedule.On(
            self.DateRules.EveryDay(self.qqq),
            self.TimeRules.AfterMarketOpen(self.qqq, 30),
            self.R,
        )

    def RecomputeWeights(self):
        # 3-month return ~ 63 trading days. Need 64 closes.
        scores = {}
        for s in self._universe:
            hist = self.History(s, 64, Resolution.Daily)
            if hist is None or hist.empty or len(hist) < 64:
                scores[s] = 0.0
                continue
            closes = hist['close'].values
            ret_3m = (closes[-1] / closes[0]) - 1.0
            scores[s] = max(0.0, float(ret_3m))

        total = sum(scores.values())
        if total <= 0.0:
            # No positive momentum names; weights all zero -> stay flat even if gate is on.
            self.weights = {s: 0.0 for s in self._universe}
        else:
            self.weights = {s: v / total for s, v in scores.items()}

        # If currently in market, push the new weights through.
        if self.in_market:
            self._apply_weights()

    def _apply_weights(self):
        for s, w in self.weights.items():
            self.SetHoldings(s, w)


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def R(self):
        hist = self.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return
        closes = hist['close'].values
        log_rets = np.diff(np.log(closes))
        vol = float(np.std(log_rets) * np.sqrt(252))

        target_in = vol < self.vol_threshold
        if target_in == self.in_market:
            return

        if target_in:
            self._apply_weights()
        else:
            self.Liquidate()

        self.in_market = target_in
