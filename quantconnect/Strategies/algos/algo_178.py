class Algo178(BaseSubAlgo):
    def initialize(self):
        self.month = None
        self.trading_day_count = 0

    def update_targets(self):
        # Get the current month (the framework should set self.current_time)
        current_month = self.current_time.month

        # Reset counter if a new month begins
        if current_month != self.month:
            self.month = current_month
            self.trading_day_count = 1
        else:
            self.trading_day_count += 1

        # Long for the first 3 trading days of the month
        if self.trading_day_count <= 3:
            weight = 1.0
        else:
            weight = 0.0

        # Apply the same weight to all symbols in the universe
        self.targets = {symbol: weight for symbol in self.symbols}
