# region imports
from AlgorithmImports import *
# endregion

class Algo093(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.symbol = self.AddEquity("TQQQ", Resolution.Daily).Symbol

    def OnData(self, data: Slice):
        if not data.ContainsKey(self.symbol):
            return

        # Get the current daily bar
        bar = data[self.symbol]
        if bar is None:
            return

        # Calculate intraday strength: (Close - Open) / Open
        open_price = bar.Open
        close_price = bar.Close
        if open_price == 0:
            return

        strength = (close_price - open_price) / open_price

        # Determine weight: if strength positive, allocate up to 100% of capital
        # Cap weight at 1.0 (no leverage). No shorting (negative strength -> weight 0)
        weight = max(0.0, min(strength, 1.0))

        # Set portfolio target
        self.SetHoldings(self.symbol, weight)
