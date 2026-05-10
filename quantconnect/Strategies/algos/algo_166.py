class Algo166(BaseSubAlgo):
    """
    Uses Williams %R with overbought/oversold thresholds.
    """
    def initialize(self):
        """Set up strategy parameters and data storage."""
        self.period = 14
        self.overbought = -20
        self.oversold = -80
        self.historical = {}   # symbol -> {'highs': [], 'lows': [], 'closes': []}

    def update_targets(self):
        """Compute Williams %R for each symbol and update trading targets."""
        targets = {}
        for symbol, bar in self.bars.items():
            high = bar['high']
            low = bar['low']
            close = bar['close']

            # Ensure historical data container exists for this symbol
            if symbol not in self.historical:
                self.historical[symbol] = {'highs': [], 'lows': [], 'closes': []}
            hist = self.historical[symbol]

            # Append current bar data
            hist['highs'].append(high)
            hist['lows'].append(low)
            hist['closes'].append(close)

            # Keep only the last `period` bars
            if len(hist['highs']) > self.period:
                hist['highs'].pop(0)
                hist['lows'].pop(0)
                hist['closes'].pop(0)

            # Not enough data yet
            if len(hist['highs']) < self.period:
                targets[symbol] = 0
                continue

            # Calculate Williams %R
            highest_high = max(hist['highs'])
            lowest_low = min(hist['lows'])
            price_range = highest_high - lowest_low
            if price_range != 0:
                w_percent_r = ((highest_high - close) / price_range) * -100
            else:
                w_percent_r = 0

            # Determine signal based on thresholds
            if w_percent_r <= self.oversold:
                targets[symbol] = 1    # Buy / overweight
            elif w_percent_r >= self.overbought:
                targets[symbol] = -1   # Sell / underweight
            else:
                targets[symbol] = 0    # Neutral

        self.targets = targets
