class Algo161(BaseSubAlgo):
    """Bollinger mean-reversion: price > 2SD expects revert."""

    def initialize(self):
        self.window = 20
        self.num_std = 2
        self.history = {}  # symbol -> list of recent prices

    def update_targets(self):
        for symbol in self.symbols:
            if symbol not in self.data:
                continue

            price = self.data[symbol]
            if price is None:
                self.targets[symbol] = 0
                continue

            # Maintain rolling price history
            if symbol not in self.history:
                self.history[symbol] = []
            self.history[symbol].append(price)
            if len(self.history[symbol]) > self.window + 1:
                self.history[symbol] = self.history[symbol][-(self.window + 1):]

            prices = self.history[symbol]
            if len(prices) < self.window:
                self.targets[symbol] = 0
                continue

            # Compute mean and std of the last `window` prices (excluding the latest if we want lagging bands)
            # Using the most recent `window` prices for the band calculation.
            window_prices = prices[-self.window:]  # e.g., last 20 closes
            mean = sum(window_prices) / self.window
            variance = sum((p - mean) ** 2 for p in window_prices) / self.window
            std = variance ** 0.5

            upper = mean + self.num_std * std
            lower = mean - self.num_std * std

            # Current price is the last price appended (the newest)
            if price > upper:
                self.targets[symbol] = -1  # short, expect revert down
            elif price < lower:
                self.targets[symbol] = 1   # long, expect revert up
            else:
                self.targets[symbol] = 0

