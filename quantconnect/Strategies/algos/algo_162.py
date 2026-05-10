class Algo162(BaseSubAlgo):
    """
    Donchian breakout strategy: goes long when price makes a new 20-day high.
    Methods:
        initialize(): sets the Donchian period and initializes data storage.
        update_targets(): computes target position based on current price.
    """

    def initialize(self):
        """Set strategy parameters and initialise rolling window for highs."""
        self.donchian_period = 20
        self.recent_highs = []  # list of high prices (most recent at end)

    def update_targets(self):
        """
        Update target position:
        - If we have enough data and current price exceeds the highest high of the last 20 bars,
          set target to 1.0 (full long), otherwise 0.0.
        """
        # Assume base class provides current price via self.current_price
        current_price = self.current_price

        # Maintain rolling window of high prices
        self.recent_highs.append(current_price)
        if len(self.recent_highs) > self.donchian_period:
            self.recent_highs.pop(0)

        # Only trade when we have a full window
        if len(self.recent_highs) == self.donchian_period:
            # Highest high of the previous 19 bars (excluding the current bar)
            prev_highs = self.recent_highs[:-1]
            if prev_highs:
                highest_prev = max(prev_highs)
                if current_price > highest_prev:
                    self.target = 1.0
                else:
                    self.target = 0.0
            else:
                self.target = 0.0
        else:
            self.target = 0.0
