from AlgorithmImports import *
from base import BaseSubAlgo, _make_standalone


class AverageIntraBarVolatility(PythonIndicator):
    def __init__(self, period):
        super().__init__()
        self.sma = SimpleMovingAverage(period)

    def Update(self, input):
        if not hasattr(input, "Open") or input.Open == 0: return False
        self.sma.Update(input.EndTime, abs((input.Open - input.Close) / input.Open) * 100)
        self.Current.Value = self.sma.Current.Value
        return self.sma.IsReady

    @property
    def Value(self): return self.Current.Value


class VolatilityBreakoutSub(BaseSubAlgo):
    def initialize(self):
        self.sym        = self.algo.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.volatility = AverageIntraBarVolatility(240)
        self.algo.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high        = self.algo.MAX(self.sym, 240, Resolution.Minute)
        self.entry_price = 0

    def on_data(self, data) -> bool:
        return self.update_targets()

    def update_targets(self) -> bool:
        if self.algo.IsWarmingUp or self.algo.Time.hour < 10: return False
        price    = self.algo.Securities[self.sym].Price
        invested = self.targets.get(self.sym, 0) > 0
        changed  = False
        if not invested:
            if self.volatility.Value < 0.1 and price >= self.high.Current.Value * 0.98:
                self.entry_price = price
                self.targets     = {self.sym: 1.0}
                changed          = True
        else:
            if self.volatility.Value > 0.15 or price <= self.entry_price * 0.97:
                self.targets = {self.sym: 0}
                changed      = True
        return changed


VolatilityBreakoutAlgo = _make_standalone(VolatilityBreakoutSub)
