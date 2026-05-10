class Algo139(BaseSubAlgo):
    """
    Strategy: Kurtosis spike detection for tail risk.
    Reduces portfolio exposure when the recent sample kurtosis of returns
    exceeds a threshold (indicating fat tails / tail risk).
    """

    def initialize(self):
        """
        Set up strategy parameters.
        """
        self.lookback = 60               # number of price bars for rolling kurtosis
        self.kurtosis_threshold = 3.0    # threshold for excess kurtosis (spike)
        self.reduction_factor = 0.5      # scale down target weight on spike

    def update_targets(self):
        """
        Compute rolling kurtosis for each symbol; reduce target weight on spikes.
        """
        for symbol in self.symbols:
            # Retrieve the last `lookback` prices from the data source
            prices = self.data.get_prices(symbol, self.lookback)
            if len(prices) < self.lookback:
                continue

            # Compute simple returns
            returns = []
            for i in range(1, len(prices)):
                ret = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(ret)

            n = len(returns)
            if n < 4:          # kurtosis is not meaningful for very small samples
                continue

            # Sample mean
            mean = sum(returns) / n

            # Sample variance (unbiased)
            var = sum((r - mean) ** 2 for r in returns) / (n - 1)
            if var == 0:       # no volatility – skip
                continue

            # Fourth central moment (biased, consistent with sample kurtosis definition)
            fourth_moment = sum((r - mean) ** 4 for r in returns) / n

            # Sample kurtosis (excess kurtosis = kurtosis - 3)
            kurtosis = fourth_moment / (var ** 2)

            # Detect spike: kurtosis above threshold (indicating fat tails)
            if kurtosis > self.kurtosis_threshold:
                # Reduce exposure – scale existing target down
                current = self.targets.get(symbol, 0.0)
                self.targets[symbol] = current * self.reduction_factor
            else:
                # Revert to normal target (equal weight on first occurrence)
                if symbol not in self.targets:
                    self.targets[symbol] = 1.0 / len(self.symbols)
