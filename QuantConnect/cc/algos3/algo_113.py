from AlgorithmImports import *

class Algo113(QCAlgorithm):
    """QuantConnect algorithm: TQQQ with Hull Moving Average regime (slope up/down)"""

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol

        # Hull Moving Average period
        self.period = 20

        # Create Hull Moving Average indicator
        self.hma = HullMovingAverage(self.period)

        # Register indicator to automatically receive data updates
        self.RegisterIndicator(self.symbol, self.hma, Resolution.Daily)

        # Store previous HMA value for slope calculation
        self.previous_hma = None

        # Warm up the indicator with historical data
        history = self.History(self.symbol, self.period, Resolution.Daily)
        for bar in history.loc[self.symbol].itertuples():
            self.hma.Update(bar.Index, bar.close)

    def OnData(self, data):
        # Ensure we have data for our symbol
        if not data.ContainsKey(self.symbol):
            return

        # Ensure indicator is ready
        if not self.hma.IsReady:
            return

        current_hma = self.hma.Current.Value

        # On first ready bar, set previous and do nothing
        if self.previous_hma is None:
            self.previous_hma = current_hma
            return

        # Determine slope direction
        slope = current_hma - self.previous_hma
        self.previous_hma = current_hma

        # Allocate based on slope regime (no leverage, weight <= 1.0)
        if slope > 0:
            self.SetHoldings(self.symbol, 1.0)
        else:
            self.SetHoldings(self.symbol, 0.0)
