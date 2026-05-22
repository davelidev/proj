from AlgorithmImports import *
import numpy as np


class Algo057(QCAlgorithm):
    """#057 — Mega-7 EW + adaptive 252d vol comparison gate (own basket)."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._Sel)
        self.SetWarmUp(280, Resolution.Daily)
        self.in_market = False
        self.Schedule.On(self.DateRules.EveryDay(self.qqq),
                         self.TimeRules.AfterMarketOpen(self.qqq, 30), self.R)

    def _vols(self):
        h = self.History(self._universe, 253, Resolution.Daily)
        if h.empty: return None, None
        rets_per_name = []
        for s in self._universe:
            try:
                if s not in h.index.get_level_values(0): return None, None
                c = h.loc[s]['close'].values
                if len(c) < 253: return None, None
                rets_per_name.append(np.diff(np.log(c)))
            except Exception:
                return None, None
        if not rets_per_name: return None, None
        arr = np.array(rets_per_name)
        basket_rets = arr.mean(axis=0)
        v20 = float(np.std(basket_rets[-20:]) * np.sqrt(252))
        v252 = float(np.std(basket_rets) * np.sqrt(252))
        return v20, v252


    def _Sel(self, fundamental):
        elig = [f for f in fundamental
                if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self._universe = [f.Symbol for f in elig[:5]]
        return self._universe

    def R(self):
        if self.IsWarmingUp: return
        v20, v252 = self._vols()
        if v20 is None: return
        gate_on = v20 < v252

        if gate_on:
            if not self.in_market:
                w = 1.0 / len(self._universe)
                for s in self._universe: self.SetHoldings(s, w)
                self.in_market = True
        else:
            if self.in_market:
                for s in self._universe:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
