from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class MomentumVoteSub(BaseSubAlgo):
    """
    Entry: TQQQ weight = n/3 bullish signals on QQQ: ROC(20)>0, up-days>10 of 20, TII(20)>10.
    Exit: weight falls to 0 as signals turn bearish.
    """

    def initialize(self):
        self.qqq  = self.algo.AddEquity("QQQ",  Resolution.Minute).Symbol
        self.tqqq = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # Get today's close up to 3:50 PM
        today_close = self.algo.Securities[self.qqq].Price

        # Fetch last 20 daily bars
        hist = self.history_daily(self.qqq, 20)
        if hist.empty or len(hist) < 20:
            return False
        
        # Append today's 3:50 PM close proxy
        closes = [float(x) for x in hist["close"].values] + [today_close]

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
        # Weighted: pure n/3
        weight = n_bullish / 3.0

        if weight > 0:
            self.targets[self.tqqq] = weight
        else:
            self.targets.pop(self.tqqq, None)


MomentumVoteAlgo = _make_standalone(MomentumVoteSub)
