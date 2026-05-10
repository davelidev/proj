class Algo186(BaseSubAlgo):
    """
    M-squared: risk-adjusted alpha strategy.
    Selects top assets by Modigliani (M²) measure relative to a benchmark.
    """
    def initialize(self):
        # Strategy parameters
        self.benchmark = 'SPY'          # Benchmark symbol (must be in universe)
        self.risk_free_rate = 0.02      # Annualized risk-free rate (2%)
        self.lookback = 252             # Number of trading days for estimation
        self.top_k = 5                  # Number of assets to hold
        self.targets = {}               # Symbol -> target weight

    def update_targets(self):
        # 1. Get benchmark prices over lookback period
        bench_prices = self.get_prices(self.benchmark, self.lookback)
        if not bench_prices or len(bench_prices) < 2:
            return  # Not enough data

        # 2. Compute benchmark daily returns
        bench_returns = []
        for i in range(1, len(bench_prices)):
            bench_returns.append(bench_prices[i] / bench_prices[i-1] - 1)

        # 3. Benchmark mean return and standard deviation (sample)
        bench_mean = sum(bench_returns) / len(bench_returns)
        bench_var = sum((r - bench_mean)**2 for r in bench_returns) / (len(bench_returns) - 1)
        bench_std = bench_var ** 0.5

        # 4. Daily risk-free rate (assume 252 trading days)
        daily_rf = self.risk_free_rate / 252

        # 5. Evaluate each asset
        asset_scores = []
        for sym in self.symbols:
            if sym == self.benchmark:
                continue
            prices = self.get_prices(sym, self.lookback)
            if not prices or len(prices) < 2:
                continue

            # Compute daily returns
            rets = []
            for i in range(1, len(prices)):
                rets.append(prices[i] / prices[i-1] - 1)

            # Mean return and std
            mean_ret = sum(rets) / len(rets)
            var = sum((r - mean_ret)**2 for r in rets) / (len(rets) - 1)
            std = var ** 0.5

            if std == 0:
                continue  # Avoid division by zero

            # M² measure
            excess_ret = mean_ret - daily_rf
            m_squared = excess_ret * (bench_std / std) + daily_rf

            asset_scores.append((sym, m_squared))

        # 6. Select top-k assets by M²
        asset_scores.sort(key=lambda x: x[1], reverse=True)
        selected = [sym for sym, _ in asset_scores[:self.top_k]]

        # 7. Equal weight allocation
        if selected:
            weight = 1.0 / len(selected)
            self.targets = {sym: weight for sym in selected}
        else:
            self.targets = {}

    def get_prices(self, symbol, lookback):
        """
        Placeholder: retrieves price history for a given symbol.
        BaseSubAlgo is expected to provide this or equivalent data access.
        """
        # In a real implementation, this method would be provided by the base class.
        # For illustration, we assume it returns a list of closing prices.
        # The user must ensure BaseSubAlgo supplies this functionality.
        return getattr(self, '_prices_data', {}).get(symbol, [])
