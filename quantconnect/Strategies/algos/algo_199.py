class Algo199(BaseSubAlgo):
    def initialize(self):
        """Add securities and store FOMC meeting dates."""
        self.symbols = []
        # Add desired equities
        for ticker in ["SPY", "QQQ"]:
            self.AddEquity(ticker)
            self.symbols.append(ticker)

        # FOMC meeting dates (first day of the meeting) for known years
        # Format: year -> list of (month, day) tuples
        self.fomc_dates = {
            2024: [(1, 30), (3, 19), (4, 30), (6, 11), (7, 30), (9, 17), (11, 6), (12, 17)],
            2025: [(1, 28), (3, 18), (5, 6),  (6, 17), (7, 29), (9, 16),  (11, 4), (12, 16)],
            # Add more years as needed
        }

    def update_targets(self):
        """Set portfolio targets: reduce to cash one day before FOMC meetings."""
        # Current date components
        y = self.Date.year
        m = self.Date.month
        d = self.Date.day

        # Compute next calendar date (skipping no trading days; simple date arithmetic)
        ny, nm, nd = self._next_date(y, m, d)

        # Check if tomorrow is an FOMC meeting day
        fomc_tuples = self.fomc_dates.get(ny, [])
        if (nm, nd) in fomc_tuples:
            # Reduce ahead of FOMC: go to cash
            self.targets = {sym: 0.0 for sym in self.symbols}
        else:
            # Normal allocation: fully invested
            self.targets = {sym: 1.0 for sym in self.symbols}

    def _next_date(self, y, m, d):
        """Return (year, month, day) of the next calendar date.
        Handles month/year boundaries and leap years."""
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        # Leap year adjustment
        if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
            days_in_month[2] = 29

        if d < days_in_month[m]:
            return y, m, d + 1
        else:
            if m == 12:
                return y + 1, 1, 1
            else:
                return y, m + 1, 1
