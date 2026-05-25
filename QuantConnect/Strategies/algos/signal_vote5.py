from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class SignalVote5Sub(BaseSubAlgo):
    """5-signal majority vote (≥3/5): CMO20, ROC20, UpDay20, TII20, Price126D."""
    def initialize(self):
        self.qqq   = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq  = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._roc  = self.algo.ROC("QQQ", 20, Resolution.Daily)
        self._sma  = self.algo.SMA("QQQ", 20, Resolution.Daily)
        self._wins = RollingWindow[float](20)

    def update_targets(self):
        if not self._roc.IsReady or not self._sma.IsReady or not self._wins.IsReady:
            return False
        h = self.algo.History(self.qqq, 126, Resolution.Daily)
        if h.empty or len(h) < 126: return False
        closes = [float(x) for x in h["close"].values]
        changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        # CMO(20)
        up  = sum(x for x in changes[-20:] if x > 0)
        dn  = sum(-x for x in changes[-20:] if x < 0)
        tot = up + dn
        cmo = 0 if tot == 0 else 100 * (up - dn) / tot
        # ROC(20)
        roc = self._roc.Current.Value > 0
        # UpDay(20)
        updays = sum(1 for x in changes[-20:] if x > 0) > 10
        # TII(20)
        sma = self._sma.Current.Value
        tii = sum(1 for i in range(20) if self._wins[i] > sma) > 10
        # Price126D
        lo, hi = min(closes), max(closes)
        p126 = (closes[-1] - lo) / (hi - lo) > 0.5 if hi != lo else False
        score = sum([cmo > 0, roc, updays, tii, p126])
        prev = dict(self.targets)
        self.targets = {self.tqqq: 1.0} if score >= 3 else {}
        return self.targets != prev

    def on_data(self, data):
        if data.Bars.ContainsKey(self.qqq):
            self._wins.Add(data.Bars[self.qqq].Close)


SignalVote5Algo = _make_standalone(SignalVote5Sub)
