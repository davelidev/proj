#region imports
from AlgorithmImports import *
#endregion


class Rebalance(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.weights = {None: 4, 'tqqq': 6}
        self.period = 'year'

        self.last = None
        for t in self.weights:
            if t is None: continue
            self.AddEquity(t, Resolution.Minute)

    def OnData(self, data):
        if self.Time.hour < 10: return
        # rebalance on start of week/month/year
        t = getattr(self.Time, self.period)
        if t == self.last: return
        self.last = t


        total = sum(self.weights.values())
        for sym, weight in self.weights.items():
            if sym is None: continue
            self.SetHoldings(sym, weight / total)
