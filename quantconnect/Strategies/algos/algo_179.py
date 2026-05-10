class Algo179(BaseSubAlgo):
    def initialize(self):
        # Define the set of symbols to trade
        self.symbols = ["SPY", "QQQ", "IWM"]  # Example tickers

    def update_targets(self):
        today = self.Time
        year = today.year
        month = today.month
        day = today.day

        # Determine the last calendar day of the current month
        last_day_of_month = self._get_last_day_of_month(year, month)

        # Rebalance only on the last day of a quarter (March, June, September, December)
        if month in [3, 6, 9, 12] and day == last_day_of_month:
            # Equal weight allocation among all symbols
            target_weight = 1.0 / len(self.symbols)
            for symbol in self.symbols:
                # Assume Portfolio[symbol].SetHoldings sets the target weight
                self.Portfolio[symbol].SetHoldings(target_weight)

    def _get_last_day_of_month(self, year, month):
        # Returns the last day of a given month, accounting for leap years
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            # Leap year: divisible by 400 or (divisible by 4 and not by 100)
            if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
                return 29
            else:
                return 28
        else:
            raise ValueError(f"Invalid month: {month}")
