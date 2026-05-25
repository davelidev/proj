from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TII20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq   = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._sma  = self.algo.SMA("QQQ", 20, Resolution.Daily)
        self._wins = RollingWindow[float](20)

    def update_targets(self):
        if not self._sma.IsReady or not self._wins.IsReady: return False
        sma = self._sma.Current.Value
        tii = sum(1 for i in range(20) if self._wins[i] > sma)
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if tii > 10 else {}
        return self.targets != prev

    def on_data(self, data):
        if data.Bars.ContainsKey(self.qqq):
            self._wins.Add(data.Bars[self.qqq].Close)


TII20Algo = _make_standalone(TII20Sub)
