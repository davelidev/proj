class Algo184(BaseSubAlgo):
    """
    Strategy: Calmar ratio (return over max drawdown).
    Allocates weights proportionally to each symbol's Calmar ratio.
    """

    def initialize(self):
        """Set lookback period for historical price data."""
        self.lookback = 252  # one trading year
        self.targets = {}

    def update_targets(self):
        """
        Compute Calmar ratio for each symbol and assign target weights
        proportional to the ratio.
        """
        # Assumes self.symbols is a list of tradable instruments
        # and self.get_prices(symbol, n) returns a list of n historical prices
        # (most recent last).
        calmar_ratios = {}

        for symbol in self.symbols:
            prices = self.get_prices(symbol, self.lookback)

            # Skip symbols with insufficient data
            if len(prices) < 2:
                calmar_ratios[symbol] = 0.0
                continue

            # Calculate cumulative total return over the lookback period
            cumulative_return = 1.0
            for i in range(1, len(prices)):
                daily_return = (prices[i] - prices[i-1]) / prices[i-1]
                cumulative_return *= (1 + daily_return)
            total_return = cumulative_return - 1.0

            # Calculate maximum drawdown (peak to trough)
            peak = prices[0]
            max_drawdown = 0.0
            for price in prices:
                if price > peak:
                    peak = price
                drawdown = (peak - price) / peak
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

            # Calmar ratio = total return / max drawdown (absolute)
            if max_drawdown > 0:
                calmar = total_return / max_drawdown
            else:
                calmar = 0.0  # No drawdown – treat as neutral

            calmar_ratios[symbol] = calmar

        # Convert ratios into target weights (sum to 1)
        total_calmar = sum(calmar_ratios.values())
        if total_calmar == 0:
            # Fallback to equal weighting
            equal_weight = 1.0 / len(self.symbols) if self.symbols else 0.0
            for symbol in self.symbols:
                self.targets[symbol] = equal_weight
        else:
            for symbol in self.symbols:
                self.targets[symbol] = calmar_ratios[symbol] / total_calmar
