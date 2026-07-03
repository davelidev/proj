from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class IBSATRStopSub(BaseSubAlgo):
    """
    Entry: TQQQ IBS<0.1 while QQQ>SMA(200) → 33% each TQQQ/SOXL/TECL.
    Exit: IBS>0.9 or 2×ATR(14) trailing stop.
    """

    ATR_MULT = 2.0

    def initialize(self):
        # Subscribe to Minute resolution for intraday tracking
        self.basket = [self.algo.AddEquity(t, Resolution.Minute).Symbol for t in ["TQQQ", "SOXL", "TECL"]]
        self.qqq = self.algo.AddEquity("QQQ", Resolution.Minute).Symbol
        self.trail = 0.0

    def update_targets(self):
        if self.algo.IsWarmingUp:
            return False

        # 1. Warmup
        today = self.get_daily_bar(self.basket[0])
        hist_qqq = self.algo.History(self.qqq, 200, Resolution.Daily)
        if today is None or len(hist_qqq) < 200:
            return False

        sma200 = sum(hist_qqq['close']) / len(hist_qqq['close'])
        in_uptrend = self.algo.Securities[self.qqq].Price > sma200

        # 3. IBS + ATR(14) on TQQQ over the last 14 daily bars + today's 3:50 PM bar
        history_daily = self.algo.History(self.basket[0], 14, Resolution.Daily)
        if len(history_daily) < 14 or today.High <= today.Low:
            return False
        ibs = (today.Close - today.Low) / (today.High - today.Low)

        hl     = list(zip(history_daily['high'], history_daily['low'])) + [(today.High, today.Low)]
        closes = list(history_daily['close']) + [today.Close]
        tr = [max(h - l, abs(h - pc), abs(l - pc))
              for (h, l), pc in zip(hl[1:], closes[:-1])]
        atr_val = sum(tr) / len(tr)

        # 4. Trading logic
        invested = self.basket[0] in self.targets
        weight = 1.0 / len(self.basket)

        if not invested:
            # Only buy the dip while QQQ is in an uptrend
            if in_uptrend and ibs < 0.1:
                self.targets = {sym: weight for sym in self.basket}
                self.trail = today.Close - self.ATR_MULT * atr_val
        else:
            # Trailing (ratcheting) 2xATR stop; exit on stop or IBS>0.9
            self.trail = max(self.trail, today.Close - self.ATR_MULT * atr_val)
            if ibs > 0.9 or today.Close < self.trail:
                self.targets = {}
                self.trail = 0.0



IBSATRStopAlgo = _make_standalone(IBSATRStopSub)
