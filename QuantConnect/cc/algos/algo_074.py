from AlgorithmImports import *

class Algo074(QCAlgorithm):
    """AVGO single-stock trend-following. Hold 100% when price > 200d SMA, else cash."""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.symbol = self.AddEquity("AVGO", Resolution.Daily).Symbol
        self.sma = self.SMA(self.symbol, 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)
        self.Schedule.On(
            self.DateRules.EveryDay("AVGO"),
            self.TimeRules.AfterMarketOpen("AVGO", 30),
            self.Rebalance,
        )

    def Rebalance(self):
        if self.IsWarmingUp or not self.sma.IsReady:
            return

        price = self.Securities[self.symbol].Price
        if price > self.sma.Current.Value:
            self.SetHoldings(self.symbol, 1.0)
        else:
            self.Liquidate(self.symbol)
