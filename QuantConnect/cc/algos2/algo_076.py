from AlgorithmImports import *

class Algo076(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100_000)

        self.tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"]
        self.symbols = {}
        self.momentum_lookback = 126

        for t in self.tickers:
            symbol = self.AddEquity(t, Resolution.Daily).Symbol
            self.symbols[t] = symbol

        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols["AAPL"]),
            self.TimeRules.AfterMarketOpen(self.symbols["AAPL"], 0),
            self._rebalance
        )

    def _rebalance(self):
        prices = self.History(list(self.symbols.values()), self.momentum_lookback + 1, Resolution.Daily)
        if prices.empty:
            return

        close = prices["close"].unstack(level=0)

        best_ticker = None
        best_momentum = -float("inf")

        for t in self.tickers:
            sym = self.symbols[t]
            if sym not in close.columns:
                continue
            series = close[sym].dropna()
            if len(series) < self.momentum_lookback + 1:
                continue

            today = series.iloc[-1]
            past = series.iloc[-(self.momentum_lookback + 1)]
            momentum = today / past - 1.0

            if momentum > best_momentum:
                best_momentum = momentum
                best_ticker = sym
            elif momentum == best_momentum:
                best_ticker = None

        for sym in self.symbols.values():
            self.Liquidate(sym)

        if best_ticker is not None:
            self.SetHoldings(best_ticker, 1.0)
