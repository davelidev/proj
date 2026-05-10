class Algo183(BaseSubAlgo):
    """
    Strategy based on Sortino ratio, preferring lower downside volatility.
    Inherits from BaseSubAlgo which provides attributes such as self.symbols,
    self.prices (dict mapping symbol -> list of prices), and self.current_weights.
    """

    def initialize(self):
        """Set parameters for Sortino ratio calculation and risk preferences."""
        self.lookback = 252               # Number of trading days for estimation
        self.risk_free_rate = 0.0        # Annual risk-free rate (assumed 0 for simplicity)
        self.target_downside_vol = 0.1   # Target annual downside volatility (10%)
        # Precompute daily risk-free rate if needed
        self.daily_rfr = self.risk_free_rate / 252.0

    def update_targets(self):
        """
        Compute target portfolio weights based on Sortino ratios.
        Returns:
            None – updates self.target_weights (dict mapping symbol -> weight)
        """
        n_symbols = len(self.symbols)
        if n_symbols == 0:
            self.target_weights = {}
            return

        sortino_ratios = {}
        for sym in self.symbols:
            prices = self.prices.get(sym, [])
            if len(prices) < self.lookback + 1:
                continue  # Not enough data, skip this symbol

            # Use the most recent lookback+1 prices to compute daily returns
            recent_prices = prices[-(self.lookback + 1):]  # last lookback+1 days
            daily_returns = []
            for i in range(1, len(recent_prices)):
                if recent_prices[i-1] != 0:
                    daily_returns.append((recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1])
                else:
                    daily_returns.append(0.0)

            if len(daily_returns) < 2:
                continue  # Insufficient returns

            # Mean return (daily)
            mean_return = sum(daily_returns) / len(daily_returns)

            # Downside deviation (only negative deviations from the risk‑free rate)
            sum_sq_neg = 0.0
            count_neg = 0
            for r in daily_returns:
                if r < self.daily_rfr:
                    diff = r - self.daily_rfr
                    sum_sq_neg += diff * diff
                    count_neg += 1

            if count_neg == 0:
                # No negative returns → extremely favorable, set downside deviation to a small positive
                downside_dev = 1e-10
            else:
                downside_dev = (sum_sq_neg / count_neg) ** 0.5

            # Sortino ratio (annualised if desired, but ratio itself is scale‑free if both numerator and denominator are daily)
            excess_return = mean_return - self.daily_rfr
            sortino_ratio = excess_return / downside_dev if downside_dev != 0 else 0.0
            sortino_ratios[sym] = sortino_ratio

        if not sortino_ratios:
            self.target_weights = {sym: 1.0 / n_symbols for sym in self.symbols}
            return

        # Allocate inversely proportional to downside volatility (or proportionally to Sortino ratio)
        # Here we use Sortino ratio directly: higher Sortino → higher weight.
        total_ratio = sum(sortino_ratios.values())
        if total_ratio <= 0:
            # Fallback to equal weight if all ratios non‑positive
            self.target_weights = {sym: 1.0 / n_symbols for sym in self.symbols}
        else:
            # Scale weights so that the portfolio downside vol matches target (simplified)
            self.target_weights = {sym: sortino_ratios.get(sym, 0.0) / total_ratio 
                                   for sym in self.symbols}
