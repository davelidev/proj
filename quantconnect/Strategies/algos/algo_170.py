class Algo170(BaseSubAlgo):
    def initialize(self):
        # CCI parameters
        self.cci_period = 20
        self.upper_threshold = 100
        self.lower_threshold = -100
        # assume self.data contains a list of typical prices (H+L+C)/3
        self.cci = None

    def update_targets(self):
        # need at least one full CCI period
        if not hasattr(self, 'data') or len(self.data) < self.cci_period:
            return

        # compute CCI for the last available bar
        typical_prices = self.data[-self.cci_period:]
        sma = sum(typical_prices) / self.cci_period
        mean_dev = sum(abs(tp - sma) for tp in typical_prices) / self.cci_period

        # avoid division by zero
        if mean_dev == 0:
            cci = 0.0
        else:
            cci = (typical_prices[-1] - sma) / (0.015 * mean_dev)

        self.cci = cci

        # set target signal based on CCI extremes
        if cci > self.upper_threshold:
            self.target = 'sell'
        elif cci < self.lower_threshold:
            self.target = 'buy'
        else:
            self.target = 'hold'
