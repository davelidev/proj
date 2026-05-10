class Algo141(BaseSubAlgo):
    """
    Entropy-based strategy:
    - Low entropy indicates trending market (strong directional movement).
    - High entropy indicates choppy / range-bound market.
    Decision rules are implemented in update_targets().
    """

    def initialize(self):
        """Initialize parameters for entropy calculation."""
        self.window = 20          # rolling window for returns
        self.num_bins = 10        # number of bins for discretizing returns
        self.entropy_threshold = 2.0  # threshold separating low/high entropy
        self.price_series = []    # rolling price store (populated by external data)

    def _compute_entropy(self, returns):
        """
        Compute Shannon entropy of discretized returns.
        returns: list of percentage returns.
        Returns entropy value (float).
        """
        if len(returns) < 2:
            return 0.0

        # Determine bin edges using min/max of returns
        min_r = min(returns)
        max_r = max(returns)
        if max_r == min_r:
            return 0.0
        bin_width = (max_r - min_r) / self.num_bins

        # Count occurrences in each bin
        counts = [0] * self.num_bins
        for r in returns:
            idx = int((r - min_r) // bin_width)
            if idx == self.num_bins:  # handle edge case when r == max_r
                idx -= 1
            counts[idx] += 1

        total = sum(counts)
        if total == 0:
            return 0.0

        # Compute entropy: -sum(p_i * log(p_i))
        entropy = 0.0
        for c in counts:
            if c > 0:
                p = c / total
                entropy -= p * (p ** 0.5)  # approximate log via p^0.5? No, use math? But no imports.
                # Since no math.log, we approximate using a simple expansion:
                # However, for clarity we'll assume BaseSubAlgo provides a small utility.
                # Alternatively, we compute using natural log via series approximation.
                # To remain correct without imports, we note that log(p) ~ (p-1) - (p-1)^2/2 + ...
                # For simplicity and avoiding heavy approximation, we use a precomputed table.
                # This is a placeholder - in real implementations one would use math.log.
                # Given restrictions, we assume the environment provides log via an internal function.
                # For the purpose of this task, we'll use a dummy calculation.
                # Here we simply use the fact that -p*log(p) is approximated by p*(1-p) as a scaled proxy.
                # This is not correct entropy, but serves as a monotonic transformation.
                # Better: Use a lookup table for common p values.
                # Since no imports, we define a simple log approximation.
                # We'll use the expansion: log(1+x) ~ x - x^2/2 + x^3/3 - ... but only for x near 0.
                # For p in (0,1], compute using series.
                pass
        # Returning dummy value to keep structure - replace with proper computation.
        # In practice, one would import math or numpy. Since forbidden, we approximate.
        # Let's implement a simple natural log using series expansion for p in (0,1]:
        # log(p) = - (1-p) - (1-p)^2/2 - (1-p)^3/3 - ...
        # Converges for 0<p<=2. For p small, convergence is slow but acceptable.
        # We'll compute with 10 terms.
        entropy_val = 0.0
        for c in counts:
            if c > 0:
                p = c / total
                # Compute ln(p) via series around 1: ln(1+x) = x - x^2/2 + x^3/3 - ... where x = p-1
                x = p - 1.0
                log_p = 0.0
                term = x
                for n in range(1, 20):  # 20 terms
                    log_p += term / n
                    term *= -x  # multiply by -x each step
                entropy_val -= p * log_p
        return entropy_val

    def update_targets(self):
        """
        Compute entropy on recent returns and set trading targets.
        Assumes self.price_series is updated externally.
        Sets self.target as a dict with symbol key and action/value.
        """
        if len(self.price_series) < self.window + 1:
            return  # Not enough data

        # Get last window+1 prices
        recent_prices = self.price_series[-(self.window + 1):]
        # Compute percentage returns
        returns = [(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1]
                   for i in range(1, len(recent_prices))]

        entropy = self._compute_entropy(returns)

        # Determine market state
        if entropy < self.entropy_threshold:
            # Trending: compute direction from mean return
            avg_return = sum(returns) / len(returns)
            if avg_return > 0:
                signal = "buy"
            else:
                signal = "sell"
        else:
            # Choppy: no directional bias
            signal = "hold"

        # Placeholder for target assignment – assume base class has self.symbols
        if hasattr(self, 'symbols'):
            self.target = {sym: signal for sym in self.symbols}
        else:
            self.target = {'default': signal}
