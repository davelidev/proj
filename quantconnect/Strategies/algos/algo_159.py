class BaseSubAlgo:
    """
    Placeholder base class. In a real framework, this would provide
    shared infrastructure (data, positions, etc.). Here we assume
    it offers at least:
        - self.data: a list/array of bars with attributes 'high', 'low', 'close'
        - self.current_index: integer pointing to the latest bar
        - self.signal: dict or number to set trading direction (+1, -1, 0)
    """
    def __init__(self):
        self.data = []          # list of bars (dict or object)
        self.current_index = -1
        self.signal = 0         # 0 = neutral, 1 = long, -1 = short

    def on_bar(self, bar):
        """Called when a new bar arrives."""
        self.data.append(bar)
        self.current_index = len(self.data) - 1
        self.update_targets()


class Algo159(BaseSubAlgo):
    """
    Strategy: Range Expansion
    Signal: ATR(20) > SMA(ATR(20)) → long (1)
            otherwise → flat (0)
    """
    def initialize(self):
        """Initialize parameters and data structures."""
        self.atr_period = 20               # period for ATR
        self.sma_period = 20               # period for SMA of ATR

        # Rolling storage for True Range values (used to compute ATR)
        self.true_ranges = []

        # Rolling storage for ATR values themselves (used to compute SMA of ATR)
        self.atr_values = []

        # For performance, we keep the current sum of true ranges and ATR values
        self.tr_sum = 0.0
        self.atr_sum = 0.0

        # Set initial signal to neutral
        self.signal = 0

    def _true_range(self, high, low, prev_close):
        """Compute True Range for a single bar."""
        return max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )

    def update_targets(self):
        """
        Called whenever a new bar arrives. It updates indicators and sets
        the trading signal.
        """
        idx = self.current_index
        if idx < 1:     # need at least two bars to compute first TR
            self.signal = 0
            return

        # Get current and previous bars
        bar = self.data[idx]
        prev_bar = self.data[idx - 1]

        # Compute True Range for the current bar
        tr = self._true_range(bar['high'], bar['low'], prev_bar['close'])
        self.true_ranges.append(tr)
        self.tr_sum += tr

        # If we have more than atr_period values, remove the oldest
        if len(self.true_ranges) > self.atr_period:
            old_tr = self.true_ranges.pop(0)
            self.tr_sum -= old_tr

        # Compute current ATR (simple average of true ranges over the period)
        if len(self.true_ranges) >= self.atr_period:
            current_atr = self.tr_sum / self.atr_period
        else:
            current_atr = None   # not enough data yet

        # If ATR is valid, store it for SMA calculation
        if current_atr is not None:
            self.atr_values.append(current_atr)
            self.atr_sum += current_atr

            # Maintain rolling window for SMA of ATR
            if len(self.atr_values) > self.sma_period:
                old_atr = self.atr_values.pop(0)
                self.atr_sum -= old_atr

        # Decide signal once we have enough ATR values to compute its SMA
        if len(self.atr_values) >= self.sma_period:
            sma_atr = self.atr_sum / self.sma_period
            if current_atr > sma_atr:
                self.signal = 1      # go long (range expansion)
            else:
                self.signal = 0      # neutral
        else:
            self.signal = 0

# Example usage (not part of the required output, just for clarity):
# algo = Algo159()
# algo.initialize()
# for bar in some_bar_list:
#     algo.on_bar(bar)
#     print(algo.signal)
