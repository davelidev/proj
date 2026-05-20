from datetime import datetime, timedelta
from AlgorithmImports import *

class Rebalance(QCAlgorithm):
    def Initialize(self):
        start_date = datetime.now() - timedelta(days=12*365)
        self.SetStartDate(start_date.year, start_date.month, start_date.day)
        self.weights = {None:4, "TQQQ": 2, "SOXL": 2, "TECL": 2}
        self.period = 'year'

        self.last = None
        for t in self.weights:
            if t is None: continue
            self.AddEquity(t, Resolution.Minute)

    def OnData(self, data):
        if self.Time.hour < 11: return
        # rebalance on start of week/month/year
        t = getattr(self.Time, self.period)
        if t == self.last: return
        self.last = t


        total = sum(self.weights.values())
        for sym, weight in self.weights.items():
            if sym is None: continue
            self.SetHoldings(sym, weight / total)
