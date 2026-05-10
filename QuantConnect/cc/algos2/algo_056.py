from AlgorithmImports import *
import numpy as np


class Algo056(QCAlgorithm):
    """#056 — Top-10 mega-cap from QC fundamental universe + basket-vol gate."""
    VOL_THRESH = 0.25

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.Sel)
        self.SetWarmUp(80, Resolution.Daily)
        self.top = []
        self.in_market = False
        self.Schedule.On(self.DateRules.EveryDay(),
                         self.TimeRules.At(10, 30), self.R)

    def Sel(self, fund):
        elig = [f for f in fund if f.HasFundamentalData and f.MarketCap > 0 and f.Price > 5]
        elig.sort(key=lambda f: f.MarketCap, reverse=True)
        self.top = [f.Symbol for f in elig[:10]]
        return self.top

    def _basket_vol(self):
        if not self.top: return None
        h = self.History(self.top, 21, Resolution.Daily)
        if h.empty: return None
        try:
            rets_per_name = []
            for s in self.top:
                if s not in h.index.get_level_values(0): continue
                c = h.loc[s]['close'].values
                if len(c) < 21: continue
                rets_per_name.append(np.diff(np.log(c)))
            if not rets_per_name: return None
            arr = np.array(rets_per_name)
            basket_rets = arr.mean(axis=0)
            return float(np.std(basket_rets) * np.sqrt(252))
        except Exception:
            return None

    def R(self):
        if self.IsWarmingUp or not self.top: return
        v = self._basket_vol()
        if v is None: return
        gate_on = v < self.VOL_THRESH

        if gate_on:
            w = 1.0 / len(self.top)
            target_set = set(self.top)
            for s in list(self.Portfolio.Keys):
                if self.Portfolio[s].Invested and s not in target_set:
                    self.Liquidate(s)
            for s in self.top: self.SetHoldings(s, w)
            self.in_market = True
        else:
            if self.in_market:
                for s in list(self.Portfolio.Keys):
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
