class Algo172(BaseSubAlgo):
    """
    Close-to-close momentum strategy: buys assets with consecutive up closes.
    """

    def initialize(self):
        """Set up the strategy parameters and initial state."""
        # Number of consecutive up closes required to generate a long signal
        self.consecutive_up_threshold = 3
        # Dictionary to store the current count of consecutive up closes per symbol
        self.consecutive_up_count = {}

    def update_targets(self):
        """
        Update target allocations based on recent price changes.
        Assumes self.symbols (list of symbols) and self.closes (dict symbol->list of close prices)
        are available from the parent class.
        """
        # Reset target weights to zero
        self.target_weights = {sym: 0.0 for sym in self.symbols}

        for symbol in self.symbols:
            # Get the close price series (most recent last)
            prices = self.closes.get(symbol, [])
            if len(prices) < 2:
                # Not enough data to determine consecutive moves
                self.consecutive_up_count[symbol] = 0
                continue

            # Compute consecutive up closes
            count = 0
            # Iterate backwards from the most recent close
            for i in range(len(prices) - 1, 0, -1):
                if prices[i] > prices[i - 1]:
                    count += 1
                else:
                    break

            self.consecutive_up_count[symbol] = count

            # Generate signal if threshold is met
            if count >= self.consecutive_up_threshold:
                self.target_weights[symbol] = 1.0

        # Normalize weights to sum to 1 (all cash if no signals)
        total_weight = sum(self.target_weights.values())
        if total_weight > 0:
            for sym in self.target_weights:
                self.target_weights[sym] /= total_weight
