class Algo168(BaseSubAlgo):
    """
    Strategy based on Accumulation/Distribution (A/D) indicator.
    Condition: A/D > 0 indicates accumulation (buy pressure).
    """
    def initialize(self):
        """
        Initialize per-symbol cumulative A/D values.
        Called once at start.
        """
        # Dictionary to store cumulative A/D for each symbol
        self.ad_line = {symbol: 0.0 for symbol in self.symbols}

    def update_targets(self):
        """
        Compute A/D for each symbol and set target weights.
        Only assign positive weight (equal allocation) if A/D > 0,
        otherwise weight is 0.
        """
        # Temporary storage for updated A/D and decision
        new_ad = {}
        target_weight = {}

        for symbol in self.symbols:
            # Get current bar: assumed as (open, high, low, close, volume)
            data = self.data.get(symbol)
            if data is None or len(data) < 5:
                continue

            high, low, close, volume = data[1], data[2], data[3], data[4]
            prev_ad = self.ad_line.get(symbol, 0.0)

            # Money Flow Volume
            if high != low:
                mfv = ((close - low) - (high - close)) / (high - low) * volume
            else:
                mfv = 0.0

            # Cumulative A/D
            new_ad[symbol] = prev_ad + mfv

            # Decision: weight = 1 (equal) if A/D > 0, else 0
            target_weight[symbol] = 1.0 if new_ad[symbol] > 0 else 0.0

        # Update stored A/D values
        self.ad_line.update(new_ad)

        # Normalize weights to sum to 1 if any positive, else all zero
        total_weight = sum(target_weight.values())
        if total_weight > 0:
            for symbol in self.symbols:
                self.target[symbol] = target_weight.get(symbol, 0.0) / total_weight
        else:
            for symbol in self.symbols:
                self.target[symbol] = 0.0
