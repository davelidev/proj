class Algo071(BaseSubAlgo):
    """
    Strategy: Top-3 sectors by 63-day return, equal-weight rebalance.
    """

    def initialize(self):
        """Add sector ETF symbols."""
        # Define a representative set of sector ETFs
        sector_etfs = [
            "XLE",  # Energy
            "XLF",  # Financials
            "XLI",  # Industrials
            "XLV",  # Health Care
            "XLK",  # Technology
            "XLP",  # Consumer Staples
            "XLY",  # Consumer Discretionary
            "XLB",  # Materials
            "XLRE", # Real Estate
            "XLC"   # Communication Services
        ]
        for symbol in sector_etfs:
            self.AddEquity(symbol, Resolution.Daily)

    def update_targets(self):
        """
        Compute 63-day returns for all sector ETFs,
        select the top 3, and set equal weights.
        """
        # Dictionary to store returns
        returns = {}

        # Get all symbols that have been added
        # (typically available via self.Securities or self.symbols)
        for symbol in self.Securities:
            # Get historical data (63 daily bars)
            hist = self.History(symbol, 63, Resolution.Daily)
            if hist.empty:
                continue

            # Access the 'close' column (pandas DataFrame returned)
            close = hist['close']
            # Compute simple return: (last close / first close) - 1
            ret = (close.iloc[-1] / close.iloc[0]) - 1
            returns[symbol] = ret

        # Sort symbols by return descending and pick top 3
        sorted_symbols = sorted(returns, key=returns.get, reverse=True)[:3]

        # Equal weight for the selected sectors
        weight = 1.0 / len(sorted_symbols) if sorted_symbols else 0.0

        # Build target dictionary
        self.targets = {sym: weight for sym in sorted_symbols}
