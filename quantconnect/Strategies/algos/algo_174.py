class Algo174(BaseSubAlgo):
    """Strategy: Highest close breakout - new 100-day high long."""

    def initialize(self):
        """Initialize algorithm parameters."""
        self.lookback = 100
        # Dictionary to store rolling windows of closing prices per symbol
        self.closes = {}

    def update_targets(self):
        """Compute and set target positions based on breakout condition."""
        for symbol in self.symbols:
            # Get current close price
            current_bar = self.bars[symbol]
            current_close = current_bar.close

            # Ensure rolling list exists for this symbol
            if symbol not in self.closes:
                self.closes[symbol] = []

            # Need at least lookback previous closes to compute the high
            if len(self.closes[symbol]) < self.lookback:
                # Not enough data – do nothing and accumulate
                self.closes[symbol].append(current_close)
                self.targets[symbol] = 0.0
                continue

            # Compute the highest close over the past lookback days (excluding current)
            past_high = max(self.closes[symbol])

            # Breakout condition: current close > highest close of previous 100 days
            if current_close > past_high:
                self.targets[symbol] = 1.0   # Full long position
            else:
                self.targets[symbol] = 0.0   # No position

            # Update rolling window: remove oldest, add current
            self.closes[symbol].pop(0)
            self.closes[symbol].append(current_close)
