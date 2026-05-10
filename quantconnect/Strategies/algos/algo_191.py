class Algo191(BaseSubAlgo):
    """
    Tail hedging strategy: reduce equity exposure on left-tail signals.
    """

    def initialize(self):
        """Add securities and initialize state."""
        # Core equity
        self.AddEquity("SPY")
        # Tail hedge instrument (e.g., long-duration Treasuries as a safe haven)
        self.AddEquity("TLT")  
        # Store historical prices for signal calculation
        self._prices = {"SPY": []}

    def update_targets(self):
        """
        Update portfolio targets based on left-tail signal.
        Signal: When SPY closes below its 200-period moving average, 
        we reduce equity exposure and increase the hedge.
        """
        # --- Calculate left-tail signal (simplified MA crossover) ---
        # Update price history
        spy_price = self.Securities["SPY"].Price
        self._prices["SPY"].append(spy_price)

        # Keep only the last 200 prices
        if len(self._prices["SPY"]) > 200:
            self._prices["SPY"].pop(0)

        # Determine if a left-tail condition exists
        if len(self._prices["SPY"]) >= 200:
            moving_avg = sum(self._prices["SPY"]) / 200
            tail_signal = spy_price < moving_avg
        else:
            tail_signal = False  # Not enough data yet

        # --- Set targets ---
        if tail_signal:
            # Left-tail event: reduce equity, increase hedge
            self.targets = {"SPY": 0.3, "TLT": 0.7}
        else:
            # Normal regime: full equity, no hedge
            self.targets = {"SPY": 1.0, "TLT": 0.0}
