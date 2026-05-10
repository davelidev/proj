class Algo079(BaseSubAlgo):
    """
    Strategy: Hold only sector ETFs that are trading above their 252-day low.
    """

    def initialize(self):
        """
        Add sector ETFs to the algorithm and initialize price history storage.
        """
        # Define the list of sector ETFs (Select Sector SPDRs)
        self.sectors = [
            "XLY",  # Consumer Discretionary
            "XLP",  # Consumer Staples
            "XLE",  # Energy
            "XLF",  # Financials
            "XLV",  # Health Care
            "XLI",  # Industrials
            "XLB",  # Materials
            "XLK",  # Technology
            "XLU",  # Utilities
            "XLC",  # Communication Services
        ]

        # Add each sector ETF to the algorithm
        for ticker in self.sectors:
            self.AddEquity(ticker)

        # Dictionary to store daily closing prices for each sector
        # Each entry is a list that will hold at most 252 historical closes
        self.price_history = {ticker: [] for ticker in self.sectors}

    def update_targets(self):
        """
        Update the portfolio targets based on the 252-day low filter.
        Only sectors up from their 252-day low are included, equally weighted.
        """
        included_sectors = []

        for ticker in self.sectors:
            # Get today's closing price for the sector ETF
            current_close = self.Securities[ticker].Close

            # Retrieve the list of historical closes (previous days)
            hist = self.price_history[ticker]

            # Check if we have at least 252 days of history
            if len(hist) >= 252:
                # Compute the 252-day low (minimum of the last 252 closes)
                low_252 = min(hist[-252:])

                # Include sector only if current price is above this low
                if current_close > low_252:
                    included_sectors.append(ticker)
            # Note: if insufficient history, the sector is not included

            # Update the historical list with today's close
            hist.append(current_close)
            # Keep only the most recent 252 closes for the next computation
            if len(hist) > 252:
                hist.pop(0)

        # Build the target weights dictionary
        if included_sectors:
            equal_weight = 1.0 / len(included_sectors)
            self.targets = {ticker: equal_weight for ticker in included_sectors}
        else:
            # If no sectors qualify, hold no positions (effectively cash)
            self.targets = {}
