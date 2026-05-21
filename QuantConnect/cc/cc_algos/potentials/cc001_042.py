from AlgorithmImports import *


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


class VolatilityBreakout(QCAlgorithm):
    """TQQQ intrabar vol breakout — enters on low-vol squeeze near 240-min high; exits on vol spike or 3% stop."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.sym        = self.AddEquity("TQQQ", Resolution.Minute).Symbol
        self.volatility = AverageIntraBarVolatility(240)
        self.RegisterIndicator(self.sym, self.volatility, Resolution.Minute)
        self.high        = self.MAX(self.sym, 240, Resolution.Minute)
        self.entry_price = 0
        self.SetWarmUp(240, Resolution.Minute)

    def OnData(self, data):
        if self.IsWarmingUp or self.Time.hour < 10: return
        if self.sym not in data or not data[self.sym]: return
        price    = self.Securities[self.sym].Price
        invested = self.Portfolio[self.sym].Invested

        if not invested:
            if (self.volatility.IsReady and self.high.IsReady
                    and self.volatility.Value < 0.1
                    and price >= self.high.Current.Value * 0.98):
                self.entry_price = price
                self.SetHoldings(self.sym, 1.0)
        else:
            if self.volatility.Value > 0.15 or price <= self.entry_price * 0.97:
                self.Liquidate(self.sym)
