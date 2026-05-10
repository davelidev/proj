class Algo180(BaseSubAlgo):
    """
    Strategy: Holiday window: days before holidays rally.
    Buys into equities when a holiday is approaching (within a defined window).
    """

    def initialize(self):
        """Set up holiday dates and window parameters."""
        # Define US holidays (month, day). In a real system, these might be configurable.
        self.holidays = [
            (1, 1),   # New Year's Day
            (1, 20),  # MLK Day (approx, simplified)
            (2, 17),  # Presidents' Day (approx)
            (5, 26),  # Memorial Day (approx)
            (7, 4),   # Independence Day
            (9, 1),   # Labor Day (approx)
            (11, 27), # Thanksgiving (approx)
            (12, 25)  # Christmas
        ]
        # Window in trading days before a holiday to enter the rally trade
        self.window_days = 5
        # Track if we have already acted for each holiday to avoid repeated entries
        self.holiday_acted = {hol: False for hol in self.holidays}

    def update_targets(self):
        """
        Update target allocations based on proximity to upcoming holidays.
        Assumes self.time (provided by BaseSubAlgo) gives current datetime.
        """
        # Check each holiday whether the current date falls within the window
        current_date = self.time.date()
        current_month = current_date.month
        current_day = current_date.day

        for holiday in self.holidays:
            month, day = holiday
            # Compute difference in days (simplistic, not calendar-accurate for month boundaries)
            # In production, use proper date arithmetic.
            holiday_date = self._build_date(month, day)
            delta = (holiday_date - current_date).days
            if 0 <= delta <= self.window_days and not self.holiday_acted[holiday]:
                # Enter rally position (example: set target allocation to 1.0 for a specific symbol)
                # The base class may have methods like self.set_target(symbol, weight)
                self.holiday_acted[holiday] = True
                # Example: self.set_target("SPY", 1.0)
            elif delta < 0:
                # After holiday passed, reset flag if desired
                self.holiday_acted[holiday] = False

    def _build_date(self, month, day):
        """Helper to build a date object for the current year."""
        import datetime
        return datetime.date(self.time.year, month, day)
