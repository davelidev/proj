from AlgorithmImports import *

class Algo071(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = {}
        self.smas = {}

        for ticker in self.tickers:
            symbol = self.AddEquity(ticker, Resolution.Daily).Symbol
            self.symbols[ticker] = symbol
            self.smas[ticker] = self.SMA(symbol, 200, Resolution.Daily)

        self.SetWarmUp(200, Resolution.Daily)

        self.Schedule.On(
            self.DateRules.MonthStart("AAPL"),
            self.TimeRules.AfterMarketOpen("AAPL", 30),
            self.Rebalance
        )

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        in_trend = []
        for ticker in self.tickers:
            symbol = self.symbols[ticker]
            sma = self.smas[ticker]
            if not sma.IsReady:
                continue
            price = self.Securities[symbol].Price
            if price > sma.Current.Value:
                in_trend.append(symbol)

        if not in_trend:
            return

        weight = 1.0 / len(in_trend)
        for symbol in in_trend:
            self.SetHoldings(symbol, weight)

        for ticker in self.tickers:
            symbol = self.symbols[ticker]
            if symbol not in in_trend:
                self.SetHoldings(symbol, 0)
