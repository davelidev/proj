class Algo188(BaseSubAlgo):
    def initialize(self):
        """
        Initialize algorithm parameters:
        - lookback period for historical data (number of bars)
        - risk-free rate (annualized, used per-bar)
        - benchmark symbol (e.g., 'SPY')
        - number of top assets to hold (based on Jensen's alpha)
        """
        self.lookback = 252          # one trading year
        self.risk_free_rate = 0.02   # 2% annual risk-free rate
        self.benchmark_symbol = 'SPY'
        self.top_n = 5

        # Call parent initializer if available
        if hasattr(super(), 'initialize'):
            super().initialize()

    def update_targets(self):
        """
        Compute Jensen's alpha for each asset using CAPM:
            alpha = actual_return - (risk_free + beta * (market_return - risk_free))
        Then set portfolio targets: equal weight in top_n assets with highest alpha,
        zero weight for all others.
        """
        # Shortcut references
        symbols = self.symbols
        benchmark = self.benchmark_symbol
        rf = self.risk_free_rate
        lookback = self.lookback

        # Get benchmark price history and compute returns
        bench_prices = self.get_price_history(benchmark, lookback)
        if len(bench_prices) < 2:
            # Not enough data → no trades
            self.targets = {sym: 0.0 for sym in symbols}
            return

        bench_returns = [
            (bench_prices[i] - bench_prices[i-1]) / bench_prices[i-1]
            for i in range(1, len(bench_prices))
        ]

        # Compute alpha for each asset
        alphas = {}
        for sym in symbols:
            prices = self.get_price_history(sym, lookback)
            if len(prices) < 2:
                continue

            # Asset returns
            returns = [
                (prices[i] - prices[i-1]) / prices[i-1]
                for i in range(1, len(prices))
            ]

            # Use the shorter of the two return series
            n = min(len(returns), len(bench_returns))
            if n == 0:
                continue

            # Means
            mean_ret = sum(returns[:n]) / n
            mean_bench = sum(bench_returns[:n]) / n

            # Covariance and variance
            cov = 0.0
            var_bench = 0.0
            for i in range(n):
                diff_ret = returns[i] - mean_ret
                diff_bench = bench_returns[i] - mean_bench
                cov += diff_ret * diff_bench
                var_bench += diff_bench ** 2

            # Beta
            beta = cov / var_bench if var_bench != 0 else 0.0

            # Jensen's alpha (using sample mean as proxy for expected returns)
            exp_ret = rf + beta * (mean_bench - rf)
            alpha = mean_ret - exp_ret
            alphas[sym] = alpha

        # Select top N assets by alpha (descending)
        sorted_symbols = sorted(alphas.items(), key=lambda x: x[1], reverse=True)
        selected = [sym for sym, _ in sorted_symbols[:self.top_n]]

        # Equal weight among selected, zero for others
        weight = 1.0 / len(selected) if selected else 0.0
        self.targets = {sym: weight for sym in selected}

        # Zero out any symbol not selected (overwrites previous targets)
        for sym in symbols:
            if sym not in selected:
                self.targets[sym] = 0.0
