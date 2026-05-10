class Algo078(BaseSubAlgo):
    """
    Strategy: Low-correlation phase → equal-weight across sector ETFs;
               High-correlation phase → concentrate in the best-performing sector.
    Methods: initialize() and update_targets()
    """
    def initialize(self):
        # List of sector ETFs
        self.sectors = [
            "XLY", "XLP", "XLE", "XLF", "XLV",
            "XLI", "XLB", "XLK", "XLU", "XLRE"
        ]
        # Add each sector ETF to the algorithm
        for sym in self.sectors:
            self.AddEquity(sym)

        # Store historical close prices for correlation calculation
        self.price_history = {sym: [] for sym in self.sectors}
        self.window = 30  # number of days to compute correlations

    def update_targets(self):
        # Update price history with current close prices
        for sym in self.sectors:
            price = self.Securities[sym].Close
            self.price_history[sym].append(price)
            # Keep only the most recent `window` prices
            if len(self.price_history[sym]) > self.window:
                self.price_history[sym].pop(0)

        # Ensure we have enough data for meaningful calculations
        min_len = min(len(v) for v in self.price_history.values())
        if min_len < 2:
            # Not enough data → equal weight
            n = len(self.sectors)
            self.targets = {sym: 1.0 / n for sym in self.sectors}
            return

        # Compute average pairwise correlation among sectors
        total_corr = 0.0
        pairs = 0
        for i in range(len(self.sectors)):
            for j in range(i + 1, len(self.sectors)):
                sym1 = self.sectors[i]
                sym2 = self.sectors[j]
                n = min(len(self.price_history[sym1]), len(self.price_history[sym2]))
                p1 = self.price_history[sym1][-n:]
                p2 = self.price_history[sym2][-n:]

                # Daily returns
                r1 = [(p1[t] - p1[t-1]) / p1[t-1] for t in range(1, n)]
                r2 = [(p2[t] - p2[t-1]) / p2[t-1] for t in range(1, n)]

                if len(r1) < 2:
                    continue

                corr = self._correlation(r1, r2)
                total_corr += corr
                pairs += 1

        avg_corr = total_corr / pairs if pairs > 0 else 0.0

        # Threshold to distinguish low vs high correlation
        threshold = 0.5

        if avg_corr < threshold:
            # Low correlation → equal weight all sectors
            n = len(self.sectors)
            self.targets = {sym: 1.0 / n for sym in self.sectors}
        else:
            # High correlation → concentrate on the sector with best window return
            best_sym = None
            best_return = -float('inf')
            for sym in self.sectors:
                prices = self.price_history[sym]
                if len(prices) >= 2:
                    ret = (prices[-1] - prices[0]) / prices[0]
                    if ret > best_return:
                        best_return = ret
                        best_sym = sym
            if best_sym is None:
                # Fallback – equal weight
                n = len(self.sectors)
                self.targets = {sym: 1.0 / n for sym in self.sectors}
            else:
                # 100% in the best sector
                self.targets = {sym: 1.0 if sym == best_sym else 0.0 for sym in self.sectors}

    def _correlation(self, x, y):
        """Compute Pearson correlation between two lists of returns."""
        n = len(x)
        if n == 0:
            return 0.0
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        if var_x == 0 or var_y == 0:
            return 0.0
        # Use **0.5 to avoid importing math
        return cov / ((var_x * var_y) ** 0.5)
