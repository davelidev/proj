from AlgorithmImports import *

class Algo110(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.lookback = 20

    def OnData(self, data):
        if not data.ContainsKey("TQQQ"):
            return

        symbol = self.Symbol("TQQQ")
        current_close = data[symbol].Close

        history = self.History(symbol, self.lookback, Resolution.Daily)
        if history.empty or len(history) < self.lookback:
            return

        high = history['high'].max()
        low = history['low'].min()
        range_length = high - low
        if range_length == 0:
            return

        threshold = low + 0.75 * range_length
        if current_close >= threshold:
            self.SetHoldings(symbol, 1.0)
        else:
            self.Liquidate(symbol)
