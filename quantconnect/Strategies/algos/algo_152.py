class Algo152(BaseSubAlgo):
    """
    Trend following strategy using Hull Moving Averages (HMA).
    Generates a continuation signal when HMA(9) > HMA(21).
    """

    def initialize(self):
        """
        Called once at the start of the algorithm.
        Initializes internal state: price history, periods, and signal.
        """
        # Hull Moving Average periods
        self.short_period = 9
        self.long_period = 21

        # Internal price list (newest at the end)
        self.prices = []

        # Current signal: None, 'long', or 'short'
        self.signal = None

    def update_targets(self, price: float) -> None:
        """
        Called every time a new price is available.
        Appends the price, recomputes HMAs, and updates the signal.

        Args:
            price (float): Current asset price.
        """
        self.prices.append(price)

        # Need at least long_period bars to compute both HMAs
        if len(self.prices) < self.long_period:
            return

        hma_short = self._hma(self.short_period)
        hma_long = self._hma(self.long_period)

        if hma_short is None or hma_long is None:
            return  # not enough data for valid HMAs

        # Update signal based on HMA comparison
        if hma_short > hma_long:
            self.signal = 'long'
        else:
            self.signal = 'short'

        # Optional: store target state (e.g., for performance tracking)
        # self.target = 1 if self.signal == 'long' else -1

    # ------------------------------------------------------------------
    # Hull Moving Average calculation helpers (no imports, pure Python)
    # ------------------------------------------------------------------

    def _wma(self, period: int) -> float | None:
        """
        Weighted Moving Average for the specified period.
        Weights: newest price gets weight = period, ..., oldest gets weight = 1.
        Returns None if not enough data.
        """
        if len(self.prices) < period:
            return None

        # Sum of prices * weights
        weighted_sum = 0.0
        total_weight = period * (period + 1) // 2

        # Loop from oldest to newest (or we can use reversed)
        start = len(self.prices) - period
        for i in range(period):
            weight = i + 1          # weight increases for newer prices
            weighted_sum += self.prices[start + i] * weight

        return weighted_sum / total_weight

    def _hma(self, period: int) -> float | None:
        """
        Hull Moving Average for the specified period.
        HMA(n) = WMA(2 * WMA(n/2) - WMA(n), sqrt(n)).
        Returns None if insufficient data.
        """
        if len(self.prices) < period:
            return None

        # n/2 and sqrt(n) rounded down to integers
        half_period = period // 2
        sqrt_period = int(period ** 0.5)

        if half_period == 0 or sqrt_period == 0:
            # Fallback: insufficient sub-periods; use a simple WMA as approximation
            return self._wma(period)

        # WMA(n) and WMA(n/2)
        wma_n = self._wma(period)
        wma_half = self._wma(half_period)
        if wma_n is None or wma_half is None:
            return None

        # Intermediate series: 2 * WMA(n/2) - WMA(n)
        intermediate = 2 * wma_half - wma_n

        # Need (sqrt_period) data points of the intermediate series to compute
        # the final WMA. But we only have a scalar intermediate value here.
        # The correct HMA computes WMA over the *series* of intermediate values,
        # not a single point. Therefore we must store the intermediate values
        # over time.

        # ------------------------------------------------------------------
        # Correct Implementation: store intermediate values in a list
        # so we can apply the final WMA over sqrt_period of them.
        # ------------------------------------------------------------------

        # Ensure we have internal storage for intermediate values
        if not hasattr(self, '_intermediate_history'):
            self._intermediate_history = []

        # Compute the intermediate value for the current bar
        self._intermediate_history.append(intermediate)

        # Trim to only keep the latest sqrt_period values
        if len(self._intermediate_history) > sqrt_period:
            self._intermediate_history = self._intermediate_history[-sqrt_period:]

        # If not enough intermediate values, cannot compute final WMA
        if len(self._intermediate_history) < sqrt_period:
            return None

        # Now apply WMA on the intermediate values (newest last)
        # Manual WMA calculation for the intermediate list
        weighted_sum = 0.0
        total_weight = sqrt_period * (sqrt_period + 1) // 2
        for i in range(sqrt_period):
            weight = i + 1
            weighted_sum += self._intermediate_history[i] * weight

        return weighted_sum / total_weight
