class Algo177(BaseSubAlgo):
    """
    Strategy: Invest at the end of the month (last 5 calendar days).
    Assumes base class provides self.year, self.month, self.day as integers.
    """

    def initialize(self):
        # No additional initialization needed for this simple strategy.
        pass

    def update_targets(self):
        """Evaluate end-of-month strength and set targets accordingly."""
        year = self.year
        month = self.month
        day = self.day

        if self._is_last_5_days(year, month, day):
            # Placeholder: set a target (e.g., full position)
            self.set_target(1.0)
        else:
            self.set_target(0.0)

    def _is_last_5_days(self, year: int, month: int, day: int) -> bool:
        """Check if the given day is within the last 5 calendar days of the month."""
        # Days in each month (non-leap year)
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # Adjust February for leap year
        if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            last_day = 29
        else:
            last_day = month_days[month - 1]

        # Last 5 days inclusive: day >= last_day - 4
        return day >= last_day - 4
