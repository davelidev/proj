class Algo156(BaseSubAlgo):
    """
    Strategy: Support test – price bounces from key levels.
    Identifies key support as the minimum price over a lookback period,
    then triggers a target when price approaches that support and bounces upward.
    """

    def initialize(self):
        """Initialize algorithm parameters and data buffers."""
        self.lookback = 20                     # number of bars to compute support
        self.bounce_threshold = 0.02           # 2% tolerance to consider price near support
        self.price_history = []                 # stores recent closing prices
        self.targets = []                       # list of (entry_price, target_price) pairs

    def update_targets(self):
        """
        Called each bar/iteration. Assumes self.prices is a list of closing prices
        (most recent last). Updates self.targets when a bounce from support occurs.
        """
        # guard: need at least 2 prices and sufficient history for lookback
        if not hasattr(self, 'prices') or len(self.prices) < 2:
            return

        current_price = self.prices[-1]
        prev_price = self.prices[-2]

        # maintain rolling price history
        self.price_history.append(current_price)
        if len(self.price_history) > self.lookback:
            self.price_history.pop(0)

        # not enough data to compute support yet
        if len(self.price_history) < self.lookback:
            return

        # support = minimum of all previous prices in the window (exclude current bar)
        support = min(self.price_history[:-1])
        if support == 0:
            return

        # check if current price is close to the support level
        distance = abs(current_price - support) / support
        if distance < self.bounce_threshold:
            # check for bounce: previous price was near or below support, current is rising
            if prev_price <= support * (1 + self.bounce_threshold) and current_price > prev_price:
                # bounce detected – set target (e.g., 5% above entry)
                target = current_price * 1.05
                self.targets.append((current_price, target))
