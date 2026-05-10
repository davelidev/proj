class Algo169(BaseSubAlgo):
    """
    Strategy: ROC acceleration - rate of change inflection.
    Detects inflection points in the Rate of Change (ROC) by computing
    its first difference (acceleration). A bullish signal occurs when
    acceleration turns from negative to positive (ROC trough), and a
    bearish signal when acceleration turns from positive to negative (ROC peak).
    """

    def initialize(self):
        """Set up strategy parameters and internal state."""
        # Period for ROC calculation
        self.roc_period = 12

        # Storage for previous ROC values (one per symbol)
        # Structure: dict {symbol: [prev_roc, prev_prev_roc]}
        # We need at least two previous ROC values to compute acceleration change.
        self._prev_rocs = {}

        # Optional: store previous acceleration to detect inflection
        self._prev_accels = {}

    def update_targets(self):
        """
        Called each time step. Updates target signals based on ROC acceleration.
        Assumes self.symbols is a list of available symbols.
        """
        # If no symbols defined, try to get from parent
        symbols = getattr(self, 'symbols', [])
        if not symbols:
            return  # Nothing to do

        for symbol in symbols:
            # Get current price – expected to be available via self.GetPrice(symbol)
            # or from self.data[symbol] structure.
            price = self.GetPrice(symbol)
            if price is None:
                continue

            # Compute current ROC: (price - price_n_periods_ago) / price_n_periods_ago
            # Need historical price from n periods ago.
            # Assuming self.GetPrice(symbol, period) returns price at given lookback.
            past_price = self.GetPrice(symbol, self.roc_period)
            if past_price is None or past_price == 0:
                # Not enough data yet – keep initial ROC as 0
                current_roc = 0.0
            else:
                current_roc = (price - past_price) / past_price

            # Initialize storage for this symbol if not present
            if symbol not in self._prev_rocs:
                self._prev_rocs[symbol] = [0.0, 0.0]  # [prev_roc, prev_prev_roc]
                self._prev_accels[symbol] = 0.0

            # Retrieve previous ROC values
            prev_roc = self._prev_rocs[symbol][0]
            prev_prev_roc = self._prev_rocs[symbol][1]

            # Compute current acceleration (first difference of ROC)
            # Acceleration = ROC(t) - ROC(t-1)
            accel = current_roc - prev_roc

            # Compute previous acceleration
            prev_accel = accel - (prev_roc - prev_prev_roc)  # alternative: prev_accel stored
            # Actually we stored prev_accel directly; simpler:
            prev_accel = self._prev_accels.get(symbol, 0.0)

            # Detect inflection:
            # - Bullish when acceleration becomes positive after being negative (trough in ROC)
            # - Bearish when acceleration becomes negative after being positive (peak in ROC)
            if prev_accel < 0 and accel > 0:
                # ROC trough -> bullish signal
                self.SetTarget(symbol, 1)      # assume 1 = buy/long
            elif prev_accel > 0 and accel < 0:
                # ROC peak -> bearish signal
                self.SetTarget(symbol, -1)     # assume -1 = sell/short
            else:
                # No inflection, hold previous target or keep neutral
                # Optionally set to 0 if no signal
                self.SetTarget(symbol, 0)

            # Update stored values for next iteration
            self._prev_rocs[symbol] = [current_roc, prev_roc]
            self._prev_accels[symbol] = accel

    # Helper methods that may be overridden from BaseSubAlgo:
    # def GetPrice(self, symbol, lookback=0): ...
    # def SetTarget(self, symbol, signal): ...
