from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class GoldenCrossATRSub(BaseSubAlgo):
    """EMA(50) > EMA(200) entry; ratcheting 3×ATR(14) trailing stop on TQQQ."""

    ATR_MULT = 3.0

    def initialize(self):
        self.qqq     = self.algo.AddEquity("QQQ",  Resolution.Daily).Symbol
        self.tqqq    = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self._ema50  = self.algo.EMA(self.qqq, 50,  Resolution.Daily)
        self._ema200 = self.algo.EMA(self.qqq, 200, Resolution.Daily)
        self._atr    = self.algo.ATR(self.tqqq, 14, MovingAverageType.Wilders, Resolution.Daily)
        self._trail  = 0.0

    def on_data(self, data):
        return self.update_targets()

    def update_targets(self):
        if not (self._ema50.IsReady and self._ema200.IsReady and self._atr.IsReady):
            return False
        tprice = self.algo.Securities[self.tqqq].Price
        bull   = self._ema50.Current.Value > self._ema200.Current.Value
        prev   = dict(self.targets)

        if not self.targets:
            if bull:
                self.targets = {self.tqqq: 1.0}
                self._trail  = tprice - self.ATR_MULT * self._atr.Current.Value
        else:
            new_trail = tprice - self.ATR_MULT * self._atr.Current.Value
            if new_trail > self._trail: self._trail = new_trail
            if tprice < self._trail or not bull:
                self.targets = {}
                self._trail  = 0.0
        return self.targets != prev


GoldenCrossATRAlgo = _make_standalone(GoldenCrossATRSub)
