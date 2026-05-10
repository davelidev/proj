class Algo133(BaseSubAlgo):
    """
    Strategy: Correlation-based pairs: long TQQQ, short SPY if corr < 0.3
    Uses rolling lookback window of 30 days (adjustable).
    """

    def initialize(self):
        """Set up symbol list and lookback period."""
        self.symbols = ['TQQQ', 'SPY']
        self.lookback = 30   # number of daily prices to use for correlation
        # Price series stored in self.prices (dict of lists), updated externally

    def update_targets(self):
        """
        Compute rolling correlation between TQQQ and SPY.
        If correlation < 0.3, go long TQQQ and short SPY.
        Otherwise, stay flat (or hold previous positions).
        """
        # Ensure we have enough price data
        if len(self.prices.get('TQQQ', [])) < self.lookback + 1 or \
           len(self.prices.get('SPY', [])) < self.lookback + 1:
            return

        # Get latest 'lookback' closing prices
        tqqq_prices = self.prices['TQQQ'][-self.lookback-1:]   # need N+1 for returns
        spy_prices  = self.prices['SPY'][-self.lookback-1:]

        # Calculate daily returns
        tqqq_returns = [(tqqq_prices[i] - tqqq_prices[i-1]) / tqqq_prices[i-1]
                        for i in range(1, len(tqqq_prices))]
        spy_returns  = [(spy_prices[i] - spy_prices[i-1]) / spy_prices[i-1]
                        for i in range(1, len(spy_prices))]

        # Compute Pearson correlation coefficient
        n = len(tqqq_returns)  # should be exactly lookback
        mean_t = sum(tqqq_returns) / n
        mean_s = sum(spy_returns) / n

        cov = sum((t - mean_t) * (s - mean_s) for t, s in zip(tqqq_returns, spy_returns))
        var_t = sum((t - mean_t) ** 2 for t in tqqq_returns)
        var_s = sum((s - mean_s) ** 2 for s in spy_returns)

        # Avoid division by zero
        if var_t == 0 or var_s == 0:
            corr = 0.0
        else:
            corr = cov / ((var_t * var_s) ** 0.5)

        # Set targets based on correlation threshold
        if corr < 0.3:
            self.targets['TQQQ'] = 1.0   # long
            self.targets['SPY']  = -1.0  # short
        else:
            # Optional: close positions or hold previous
            # Here we set to 0 to exit any existing positions
            self.targets['TQQQ'] = 0.0
            self.targets['SPY']  = 0.0
