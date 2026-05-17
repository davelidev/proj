from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class TQQQTechDipSub(BaseSubAlgo):
    """TQQQ version of tech_dip: RSI(2) < 30 & Price > SMA(50)."""

    def initialize(self):
        self.sym = self.algo.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.rsi = self.algo.RSI(self.sym, 2)
        self.max = self.algo.MAX(self.sym, 252)
        self.sma50 = self.algo.SMA(self.sym, 50)

    def update_targets(self):
        if not (self.max.IsReady and self.sma50.IsReady): return False
        
        prev = dict(self.targets)
        sec = self.algo.Securities[self.sym]
        price = sec.Price

        if not sec.Invested:
            if self.rsi.Current.Value < 30 and price > self.sma50.Current.Value:
                self.targets[self.sym] = 1.0
        else:
            # Exit conditions: 15% stop loss or 1-year high
            avg_price = sec.Holdings.AveragePrice
            if price <= avg_price * 0.85 or price >= self.max.Current.Value:
                self.targets.pop(self.sym, None)
            else:
                # Maintain position
                self.targets[self.sym] = 1.0

        return self.targets != prev


TQQQTechDipAlgo = _make_standalone(TQQQTechDipSub)
