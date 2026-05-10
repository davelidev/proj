from AlgorithmImports import *
import numpy as np


class Algo052(QCAlgorithm):
    """#052 — Mega-7 EW + own-basket vol gate (basket vol < 25%)."""
    VOL_THRESH = 0.25
    MEGA = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)
        self.syms = [self.AddEquity(t, Resolution.Daily).Symbol for t in self.MEGA]
        self.SetWarmUp(80, Resolution.Daily)
        self.in_market = False
        self.Schedule.On(self.DateRules.EveryDay(self.syms[0]),
                         self.TimeRules.AfterMarketOpen(self.syms[0], 30), self.R)

    def _basket_vol(self):
        h = self.History(self.syms, 21, Resolution.Daily)
        if h.empty: return None
        rets_per_day = []
        try:
            for s in self.syms:
                if s not in h.index.get_level_values(0): return None
                c = h.loc[s]['close'].values
                if len(c) < 21: return None
                rets_per_day.append(np.diff(np.log(c)))
        except Exception:
            return None
        if not rets_per_day: return None
        rets_per_day = np.array(rets_per_day)
        # Equal-weight basket return per day = average of name returns
        basket_rets = rets_per_day.mean(axis=0)
        return float(np.std(basket_rets) * np.sqrt(252))

    def R(self):
        if self.IsWarmingUp: return
        v = self._basket_vol()
        if v is None: return
        gate_on = v < self.VOL_THRESH

        if gate_on:
            if not self.in_market:
                w = 1.0 / len(self.syms)
                for s in self.syms: self.SetHoldings(s, w)
                self.in_market = True
        else:
            if self.in_market:
                for s in self.syms:
                    if self.Portfolio[s].Invested: self.Liquidate(s)
                self.in_market = False
