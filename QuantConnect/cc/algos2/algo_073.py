from AlgorithmImports import *

class Algo073(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
        self.symbols = [self.AddEquity(t, Resolution.Daily).Symbol for t in tickers]

        self.Schedule.On(
            self.DateRules.EveryDay("AAPL"),
            self.TimeRules.AfterMarketOpen("AAPL", 30),
            self.ComputeIBSAndRebalance
        )

    def ComputeIBSAndRebalance(self):
        ibs = {}
        for symbol in self.symbols:
            history = self.History(symbol, 2, Resolution.Daily)
            if history.empty:
                continue
            bar = history.iloc[-1]
            high, low, close = bar["high"], bar["low"], bar["close"]
            ibs[symbol] = 0.5 if high == low else (close - low) / (high - low)

        if not ibs:
            return

        long_symbols = [s for s, v in ibs.items() if v < 0.5]
        weight = 1.0 / len(long_symbols) if long_symbols else 0

        for symbol in self.symbols:
            self.SetHoldings(symbol, weight if symbol in long_symbols else 0)
