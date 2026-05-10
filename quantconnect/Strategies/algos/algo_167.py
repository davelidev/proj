class Algo167(BaseSubAlgo):
    """
    Strategy: On-balance volume: OBV > MA(OBV) confirmation.
    """
    def initialize(self):
        """Setup data and parameters for the strategy."""
        self.symbol = "SPY"                     # Example symbol
        self.ma_period = 20                     # Moving average period for OBV
        self.add_data(self.symbol)              # Register data feed (base class method)

        # State variables
        self.prev_close = None                  # Previous close price
        self.obv = 0                            # Current OBV value (cumulative)
        self.obv_history = []                   # Rolling list of OBV values for MA
        self.signal = 0                         # Current trading signal: 1=bullish, -1=bearish, 0=neutral

    def update_targets(self):
        """Update target position based on OBV > MA(OBV) confirmation."""
        data = self.get_data(self.symbol)       # Get current bar data (base class method)
        close = data['close']
        volume = data['volume']

        # First bar: initialise previous close and OBV
        if self.prev_close is None:
            self.prev_close = close
            self.obv = 0
            self.obv_history.append(0)
            self.target = 0                     # No position yet
            return

        # Update OBV: add/subtract volume based on price direction
        if close > self.prev_close:
            self.obv += volume
        elif close < self.prev_close:
            self.obv -= volume
        # else: unchanged close, OBV stays same
        self.prev_close = close

        # Maintain rolling OBV history
        self.obv_history.append(self.obv)
        if len(self.obv_history) > self.ma_period:
            self.obv_history.pop(0)

        # Compute signal if enough history
        if len(self.obv_history) >= self.ma_period:
            ma_obv = sum(self.obv_history) / self.ma_period
            self.signal = 1 if self.obv > ma_obv else -1
        else:
            self.signal = 0

        # Set target position (e.g., as fraction of portfolio)
        self.target = self.signal               # Base class uses self.target to set position
