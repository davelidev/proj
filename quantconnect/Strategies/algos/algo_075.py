class Algo075(BaseSubAlgo):
    """
    Daily sector rotation strategy.
    Ranks sector ETFs by their 252-day return,
    invests equally in the top 3 each day.
    """

    def initialize(self) -> None:
        """Set up algorithm: dates, cash, resolution, and sector ETFs."""
        self.SetResolution(Resolution.Daily)

        # Define sector ETF symbols (common US sector funds)
        self.sector_symbols = [
            "XLB",  # Materials
            "XLE",  # Energy
            "XLF",  # Financials
            "XLI",  # Industrials
            "XLK",  # Technology
            "XLP",  # Consumer Staples
            "XLU",  # Utilities
            "XLV",  # Health Care
            "XLY",  # Consumer Discretionary
            "XLC"   # Communication Services
        ]

        # Add all sector ETFs to the algorithm
        for symbol in self.sector_symbols:
            self.AddEquity(symbol, Resolution.Daily)

    def update_targets(self) -> None:
        """
        Compute 252-day return for each sector ETF,
        select top 3, set equal weights.
        """
        # We need at least 252 trading days of history
        if self.Time is None:
            return

        # Get 252 days of daily history for all symbols
        history = self.History(self.sector_symbols, 252, Resolution.Daily)
        if history.empty:
            return

        # Extract closing prices: the DataFrame has multi-index (time, symbol)
        close_df = history['close'].unstack(level=1)

        # Ensure we have enough data (at least 252 rows)
        if close_df.shape[0] < 252:
            return

        # Compute trailing 252-day return: (last close / first close) - 1
        # first close is the oldest in the window, last is the most recent
        first_close = close_df.iloc[0]
        last_close = close_df.iloc[-1]
        returns = (last_close / first_close) - 1.0

        # Sort by return descending
        sorted_returns = returns.sort_values(ascending=False)

        # Select top 3 sectors
        top_n = 3
        top_symbols = sorted_returns.head(top_n).index.tolist()

        # Equal weight for top sectors, zero for others
        weight = 1.0 / top_n
        self.targets = {}
        for sym in self.sector_symbols:
            self.targets[sym] = weight if sym in top_symbols else 0.0
