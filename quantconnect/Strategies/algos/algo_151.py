class Algo151(BaseSubAlgo):
    """
    Swing trading strategy: buy pullbacks, sell rallies.
    Tracks recent highs and lows to generate signals.
    """

    def initialize(self):
        """Initialize state variables."""
        self.high_price = None
        self.low_price = None
        self.buy_signal = False
        self.sell_signal = False
        # Pullback and rally thresholds (percentages)
        self.pullback_threshold = -0.05   # -5% drop from high
        self.rally_threshold = 0.05       # +5% rise from low

    def update_targets(self):
        """
        Update price extremes and generate buy/sell signals.
        Assumes self.current_price is available from parent class.
        """
        price = self.current_price

        # Initialize extremes on first call
        if self.high_price is None or self.low_price is None:
            self.high_price = price
            self.low_price = price
            return

        # Update recent high and low
        if price > self.high_price:
            self.high_price = price
        if price < self.low_price:
            self.low_price = price

        # Generate buy signal: price pulled back from recent high
        if price <= self.high_price * (1 + self.pullback_threshold):
            self.buy_signal = True
        else:
            self.buy_signal = False

        # Generate sell signal: price rallied from recent low
        if price >= self.low_price * (1 + self.rally_threshold):
            self.sell_signal = True
        else:
            self.sell_signal = False
