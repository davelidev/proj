class Algo155(BaseSubAlgo):
    """
    Breakout Fade Strategy: Quick reversal after a breakout.
    - Detects break above recent high (resistance) or break below recent low (support).
    - Expects a quick reversal back within the range and fades the breakout.
    - Generates target weights: short when breaking above resistance, long when breaking below support.
    """

    def initialize(self):
        """Initialize strategy parameters and state."""
        # Number of periods for reference high/low
        self.lookback = 20
        # Dictionary storing recent highs for each symbol
        self.recent_high = {}
        # Dictionary storing recent lows for each symbol
        self.recent_low = {}
        # Dictionary storing current position state: 'neutral', 'short', 'long'
        self.position_state = {}
        # Dictionary storing the price at which breakout was triggered
        self.entry_price = {}
        # Threshold as a fraction to confirm reversal (e.g., 0.001 for 0.1%)
        self.reversal_threshold = 0.001

    def update_targets(self):
        """
        Update target weights based on new bar data.
        Assumes self.symbols and self.bars are available from BaseSubAlgo context.
        """
        if not hasattr(self, 'bars') or self.bars is None:
            return

        for symbol in self.symbols:
            if symbol not in self.recent_high:
                # Initialize with current bar's high/low
                bar = self.bars[symbol]
                self.recent_high[symbol] = bar.high
                self.recent_low[symbol] = bar.low
                self.position_state[symbol] = 'neutral'
                self.entry_price[symbol] = 0.0
                continue

            # Update rolling high/low (simple: keep the max/min over lookback periods)
            # For simplicity, we maintain a list of recent bars here (could be optimized)
            # But since we only have method calls, we'll keep a running window.
            # We'll store a list of highs/lows per symbol (initialized in first call if needed)
            if not hasattr(self, '_high_list'):
                self._high_list = {s: [] for s in self.symbols}
                self._low_list = {s: [] for s in self.symbols}

            bar = self.bars[symbol]
            high = bar.high
            low = bar.low

            # Append new values and maintain lookback length
            self._high_list[symbol].append(high)
            self._low_list[symbol].append(low)
            if len(self._high_list[symbol]) > self.lookback:
                self._high_list[symbol].pop(0)
                self._low_list[symbol].pop(0)

            # Compute current reference levels
            current_high_ref = max(self._high_list[symbol])
            current_low_ref = min(self._low_list[symbol])
            current_price = bar.close

            # Update stored reference levels for breakout detection
            prev_high = self.recent_high[symbol]
            prev_low = self.recent_low[symbol]

            # --- Breakout fade logic ---
            # If we have an open position, check for reversal exit
            if self.position_state[symbol] == 'short':
                # We entered short after a resistance breakout; exit if price closes back below resistance
                if current_price < prev_high:
                    # Reversal occurred -> close short (target weight 0)
                    self.set_target(symbol, 0)
                    self.position_state[symbol] = 'neutral'
                    self.entry_price[symbol] = 0.0
                # else hold short (target weight -1 or fraction)
            elif self.position_state[symbol] == 'long':
                # We entered long after a support breakdown; exit if price closes back above support
                if current_price > prev_low:
                    # Reversal occurred -> close long
                    self.set_target(symbol, 0)
                    self.position_state[symbol] = 'neutral'
                    self.entry_price[symbol] = 0.0
                # else hold long
            else:
                # Neutral: look for breakout signals
                # Resistance breakout fade: price breaks above recent high, then we wait for a small pullback
                # For simplicity, we fade immediately with a tight reversal confirmation.
                if current_price > prev_high * (1 + self.reversal_threshold):
                    # Price broke above resistance; anticipate quick reversal -> short
                    self.set_target(symbol, -1)   # e.g., 100% short (adjust weight as needed)
                    self.position_state[symbol] = 'short'
                    self.entry_price[symbol] = current_price
                elif current_price < prev_low * (1 - self.reversal_threshold):
                    # Price broke below support; anticipate quick reversal -> long
                    self.set_target(symbol, 1)    # 100% long
                    self.position_state[symbol] = 'long'
                    self.entry_price[symbol] = current_price
                else:
                    self.set_target(symbol, 0)

            # Update stored reference levels for next bar
            self.recent_high[symbol] = current_high_ref
            self.recent_low[symbol] = current_low_ref

    def set_target(self, symbol, weight):
        """Helper to set target weight (if BaseSubAlgo provides a method, override accordingly)."""
        # Assume BaseSubAlgo has a 'targets' dict or method; we'll simulate.
        # In real QC, you'd use self.SetHoldings(symbol, weight).
        # For this abstract class, we just store.
        if not hasattr(self, '_targets'):
            self._targets = {}
        self._targets[symbol] = weight
