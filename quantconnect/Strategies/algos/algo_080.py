class Algo080(BaseSubAlgo):
    """
    Strategy: Detect sector divergence by comparing recent price returns,
    then concentrate allocation on the sector leader (highest return).
    Implements methods:
      - initialize(): adds a predefined set of sector ETFs via self.AddEquity().
      - update_targets(): sets self.targets with symbol->weight mapping.
    """
    def initialize(self):
        # Define sector ETFs (representative of major US sectors)
        self.sector_etfs = [
            'XLI',   # Industrials
            'XLK',   # Technology
            'XLV',   # Healthcare
            'XLE',   # Energy
            'XLF',   # Financials
            'XLY',   # Consumer Discretionary
            'XLP',   # Consumer Staples
            'XLU',   # Utilities
            'XLB',   # Materials
            'XLRE'   # Real Estate
        ]
        # Add each ETF to the algorithm
        for etf in self.sector_etfs:
            self.AddEquity(etf)

        # Dictionary to store historical closing prices for each ETF
        self.price_history = {etf: [] for etf in self.sector_etfs}

        # Lookback period for return calculation (e.g., 20 trading days)
        self.lookback = 20

    def update_targets(self):
        # Flags to ensure we have enough data for all symbols
        enough_data = True

        # Update price histories with current close prices
        for etf in self.sector_etfs:
            # Access current security's closing price
            current_price = float(self.Securities[etf].Close)
            self.price_history[etf].append(current_price)

            # Keep only the latest `lookback` prices to save memory
            if len(self.price_history[etf]) > self.lookback:
                self.price_history[etf].pop(0)

            # Check if we have at least `lookback` prices
            if len(self.price_history[etf]) < self.lookback:
                enough_data = False

        # If insufficient data, set equal weights (fallback)
        if not enough_data:
            weight = 1.0 / len(self.sector_etfs)
            self.targets = {etf: weight for etf in self.sector_etfs}
            return

        # Compute simple returns over the lookback period
        # return = (current_price / price_lookback_ago) - 1
        returns = {}
        for etf in self.sector_etfs:
            prices = self.price_history[etf]
            # prices list is ordered oldest to newest (index 0 = oldest)
            # length is exactly `lookback` after the check above
            start_price = prices[0]
            end_price = prices[-1]
            returns[etf] = (end_price / start_price) - 1.0

        # Identify the sector with the highest return (leader)
        leader = max(returns, key=returns.get)

        # Concentrate allocation: 100% on the leader, 0% on others
        self.targets = {etf: 1.0 if etf == leader else 0.0 for etf in self.sector_etfs}
