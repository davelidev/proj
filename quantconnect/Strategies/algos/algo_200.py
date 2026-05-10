class Algo200(BaseSubAlgo):
    """
    Strategy: Earnings season - avoid week before earnings.
    
    In initialize(), add equities for a predefined universe.
    In update_targets(), set portfolio targets:
        - Zero weight for any stock whose next earnings date falls within the next 7 days.
        - Equally weight all other stocks.
    """

    # Define universe and their earnings dates (date as datetime object, provided by the environment)
    EARNINGS = {
        "AAPL": [datetime(2025, 4, 24), datetime(2025, 7, 24), datetime(2025, 10, 23)],
        "MSFT": [datetime(2025, 4, 29), datetime(2025, 7, 29), datetime(2025, 10, 28)],
        "GOOGL": [datetime(2025, 4, 23), datetime(2025, 7, 23), datetime(2025, 10, 22)],
        # ... additional tickers can be added
    }

    def initialize(self):
        # Add all securities from the universe
        for ticker in self.EARNINGS:
            self.AddEquity(ticker)

    def update_targets(self):
        current_time = self.Time  # datetime object provided by base class
        targets = {}

        # Determine which securities are in earnings week (within 7 days before any earnings date)
        avoid = set()
        for ticker, dates in self.EARNINGS.items():
            for earn_date in dates:
                days_until = (earn_date - current_time).days
                if 0 <= days_until <= 7:  # within the next 7 days (including today)
                    avoid.add(ticker)
                    break

        # Compute equal weight for the remaining securities
        safe_tickers = [t for t in self.EARNINGS if t not in avoid]
        if safe_tickers:
            weight = 1.0 / len(safe_tickers)
            for ticker in safe_tickers:
                targets[ticker] = weight

        # Securities in the avoid list get zero weight (implicitly by omission or set to 0)
        for ticker in avoid:
            targets[ticker] = 0

        self.targets = targets
