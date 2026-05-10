class Algo144(BaseSubAlgo):
    """
    Regime-aware leverage strategy: increases leverage in low-volatility regimes
    and decreases it in high-volatility regimes.

    Requires the parent class to provide:
    - self.symbols: list of trading symbols
    - self.current_price: latest price for the primary asset (or first symbol)
    """

    def initialize(self):
        """
        Set strategy parameters and initialize state.
        """
        # ---- Leverage bounds ----
        self.max_leverage = 3.0   # maximum allowed leverage
        self.min_leverage = 1.0   # minimum allowed leverage

        # ---- Volatility thresholds (annualized) ----
        self.low_vol_threshold = 0.08   # below this → high leverage
        self.high_vol_threshold = 0.18  # above this → low leverage

        # ---- Lookback window for volatility estimation (days) ----
        self.vol_window = 20

        # ---- Internal state: price history for the benchmark asset ----
        self.price_history = []

        # ---- Initial leverage and targets (to be updated) ----
        self.leverage = 1.0
        # Set equal target weights for all symbols (sum to 1)
        n = len(self.symbols)
        self.targets = {sym: 1.0 / n for sym in self.symbols}

    def update_targets(self):
        """
        Update leverage based on recent volatility and keep target weights constant.
        """
        # 1. Append the most recent price (assumed available as self.current_price)
        if not hasattr(self, 'current_price') or self.current_price is None:
            return  # cannot compute volatility without price data
        self.price_history.append(self.current_price)

        # 2. Compute volatility only if enough history
        if len(self.price_history) < self.vol_window + 1:
            # Not enough data → keep current leverage
            return

        # 3. Calculate daily returns over the last `vol_window` days
        recent_prices = self.price_history[-self.vol_window-1:]
        daily_returns = []
        for i in range(1, len(recent_prices)):
            if recent_prices[i-1] == 0:
                continue
            daily_returns.append(recent_prices[i] / recent_prices[i-1] - 1.0)

        if len(daily_returns) < 2:
            return  # not enough returns to compute meaningful std

        # 4. Compute sample standard deviation of daily returns
        mean_ret = sum(daily_returns) / len(daily_returns)
        variance = sum((r - mean_ret) ** 2 for r in daily_returns) / (len(daily_returns) - 1)
        daily_vol = variance ** 0.5

        # Annualize volatility (252 trading days)
        annual_vol = daily_vol * (252 ** 0.5)

        # 5. Determine leverage based on regime
        if annual_vol < self.low_vol_threshold:
            # Low volatility → high leverage
            new_leverage = self.max_leverage
        elif annual_vol > self.high_vol_threshold:
            # High volatility → low leverage
            new_leverage = self.min_leverage
        else:
            # Intermediate: linearly interpolate between min and max
            fraction = (annual_vol - self.low_vol_threshold) / (self.high_vol_threshold - self.low_vol_threshold)
            new_leverage = self.max_leverage - fraction * (self.max_leverage - self.min_leverage)

        # 6. Update the strategy's leverage (target weights remain equal)
        self.leverage = new_leverage

        # (Optional: keep target weights unchanged; they are already set in initialize())
        # Note: self.targets dict is not modified here, only the global leverage changes.
