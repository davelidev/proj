class Algo140(BaseSubAlgo):
    """
    Strategy: Liquidity-adjusted entry. Only trade if the bid-ask spread
    is less than 0.5 basis points (0.5 bps = 0.00005).
    """

    def initialize(self):
        """Initialize strategy parameters."""
        self.spread_threshold = 0.00005  # 0.5 bps in decimal

    def update_targets(self):
        """
        Evaluate current spread for each tracked symbol.
        If spread < 0.5 bps, set a target (here, a simple buy/sell signal).
        Otherwise, clear any existing target.
        """
        for symbol in self.symbols:
            if self._spread_below_threshold(symbol):
                # Example: set target to buy 100 shares when condition met
                self.set_target(symbol, 100)
            else:
                # Remove target if spread too wide
                self.clear_target(symbol)

    def _spread_below_threshold(self, symbol):
        """
        Helper to check if the current bid-ask spread is below threshold.
        Assumes the data source provides 'bid' and 'ask' for the symbol.
        """
        try:
            bid = self.current_data[symbol].bid
            ask = self.current_data[symbol].ask
            if bid <= 0:
                return False
            spread = (ask - bid) / bid
            return spread < self.spread_threshold
        except (KeyError, AttributeError, ZeroDivisionError):
            return False
