# region imports
from AlgorithmImports import *
# endregion

class Algo085(QCAlgorithm):
    """
    Strategy: Dispersion weighting.
    Universe: A set of major ETFs (SPY, QQQ, IWM, EFA, EEM).
    Each day, compute the cross-sectional standard deviation of daily returns across the universe.
    If the current spread (standard deviation) exceeds the historical median (over a 252-day lookback),
    then allocate equal weight to all assets. Otherwise, hold no positions (cash).
    Rebalance daily.
    """
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 1, 1)
        self.SetCash(100000)

        # Universe of ETFs
        self.tickers = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
        for ticker in self.tickers:
            self.AddEquity(ticker, Resolution.Daily)

        # For rolling median of spreads
        self.lookback = 252
        self.spreads = []  # will store daily spread values

        # Store previous day's close for each symbol
        self.previous_close = {}

    def OnData(self, data):
        # Collect current close prices for all symbols that have data
        current_close = {}
        for ticker in self.tickers:
            if ticker in data.Bars:
                current_close[ticker] = data.Bars[ticker].Close

        # Need at least two symbols with data to compute spread
        if len(current_close) < 2:
            return

        # Compute daily returns for symbols that have previous close
        returns = []
        for ticker, price in current_close.items():
            if ticker in self.previous_close and self.previous_close[ticker] != 0:
                ret = (price - self.previous_close[ticker]) / self.previous_close[ticker]
                returns.append(ret)

        # Need at least two returns to compute spread
        if len(returns) < 2:
            # Update previous close and skip trading
            self.previous_close = current_close.copy()
            return

        # Compute cross-sectional spread (standard deviation of returns)
        spread = np.std(returns, ddof=0)  # population std
        self.spreads.append(spread)

        # Limit the spread history to lookback period
        if len(self.spreads) > self.lookback:
            self.spreads.pop(0)

        # Only trade if we have enough history to compute median
        if len(self.spreads) < self.lookback:
            # Not enough data yet, skip trading
            self.previous_close = current_close.copy()
            # Optional: hold nothing
            for ticker in self.tickers:
                self.SetHoldings(ticker, 0)
            return

        # Compute median of past spreads
        median_spread = np.median(self.spreads)

        # Strategy logic
        if spread > median_spread:
            # Equal weight all symbols that have data
            n = len(current_close)
            weight = 1.0 / n if n > 0 else 0
            for ticker in self.tickers:
                if ticker in current_close:
                    self.SetHoldings(ticker, weight)
                else:
                    self.SetHoldings(ticker, 0)
        else:
            # No position (cash)
            for ticker in self.tickers:
                self.SetHoldings(ticker, 0)

        # Update previous close for next day
        self.previous_close = current_close.copy()
