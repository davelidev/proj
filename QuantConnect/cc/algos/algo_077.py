from AlgorithmImports import *

class Algo077(QCAlgorithm):
    """TQQQ Z-score mean reversion.
    Buy TQQQ at 100% when Z < -2 (extreme oversold relative to 20-day
    mean). Exit the position when Z crosses back above zero.
    """

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        self.sma = self.SMA(self.tqqq, 20, Resolution.Daily)
        self.std = self.STD(self.tqqq, 20, Resolution.Daily)

        self.SetWarmUp(20, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay("TQQQ"),
            self.TimeRules.AfterMarketOpen("TQQQ", 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady or not self.std.IsReady:
            return

        price = self.Securities[self.tqqq].Close
        z = (price - self.sma.Current.Value) / self.std.Current.Value

        if z < -2.0:
            self.SetHoldings(self.tqqq, 1.0)
        elif z > 0.0:
            self.Liquidate(self.tqqq)
