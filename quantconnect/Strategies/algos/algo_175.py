class Algo175(BaseSubAlgo):
    """
    Strategy: Lowest close support - hold above 100-day low.
    """
    def initialize(self):
        self.closes = []
        self.lowest_100d = None

    def update_targets(self):
        # Get current close price (assumed available in self.ctx)
        close = self.ctx.close
        self.closes.append(close)
        # Keep only the last 100 closes
        if len(self.closes) > 100:
            self.closes.pop(0)
        # Wait until we have 100 data points
        if len(self.closes) == 100:
            self.lowest_100d = min(self.closes)
            # If current close is above the 100-day low, go long; otherwise flat
            self.target = 1 if close > self.lowest_100d else 0
        else:
            self.target = 0
