from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MomentumVoteSub(BaseSubAlgo):
    """TQQQ weight = n/3 where n = bullish count among ROC(20)>0, UpDay(20)>10, TII(20)>10."""

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol

    def update_targets(self):
        hist = self.algo.History(self.qqq, 21, Resolution.Daily)
        if hist.empty or len(hist) < 21:
            return False
        closes = [float(x) for x in hist["close"].values]

        # ROC(20): is today's close higher than 20 days ago?
        sig_roc = closes[-1] > closes[0]

        # UpDay(20): more than half of last 20 day-to-day changes positive
        up_days = sum(1 for i in range(1, len(closes)) if closes[i] > closes[i-1])
        sig_upday = up_days > 10

        # TII(20): more than half of last 20 closes above their SMA(20)
        last_20 = closes[-20:]
        sma_20  = sum(last_20) / 20
        n_above = sum(1 for c in last_20 if c > sma_20)
        sig_tii = n_above > 10

        n_bullish = sig_roc + sig_upday + sig_tii
        weight = n_bullish / 3.0

        prev = dict(self.targets)
        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)
        return self.targets != prev


MomentumVoteAlgo = _make_standalone(MomentumVoteSub)
