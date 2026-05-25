from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class CMO20Sub(BaseSubAlgo):
    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        h = self.algo.History(self.qqq, 21, Resolution.Daily)
        if h.empty or len(h) < 21: return False
        c = [float(x) for x in h["close"].values]
        changes = [c[i] - c[i-1] for i in range(1, len(c))]
        up  = sum(x for x in changes if x > 0)
        dn  = sum(-x for x in changes if x < 0)
        tot = up + dn
        cmo = 0 if tot == 0 else 100 * (up - dn) / tot
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if cmo > 0 else {}
        return self.targets != prev


CMO20Algo = _make_standalone(CMO20Sub)
