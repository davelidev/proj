class Algo164(BaseSubAlgo):
    def initialize(self, **kwargs):
        # MACD parameters
        self.fast = kwargs.get('fast', 12)
        self.slow = kwargs.get('slow', 26)
        self.signal = kwargs.get('signal', 9)

        # State for crossover detection
        self.prev_macd = None
        self.prev_signal = None
        self.prices = []
        self.macd_values = []

    def update_targets(self):
        # Ensure we have a current price
        if not hasattr(self, 'data') or not hasattr(self.data, 'current'):
            return

        price = self.data.current
        self.prices.append(price)

        # Need at least slow period + signal period bars for reliable indicators
        if len(self.prices) < self.slow + self.signal:
            return

        # Helper function to compute EMA (exponential moving average)
        def ema(data, period):
            multiplier = 2.0 / (period + 1.0)
            result = [data[0]]
            for i in range(1, len(data)):
                ema_val = (data[i] - result[-1]) * multiplier + result[-1]
                result.append(ema_val)
            return result

        # Compute MACD line
        fast_ema = ema(self.prices, self.fast)[-1]
        slow_ema = ema(self.prices, self.slow)[-1]
        macd = fast_ema - slow_ema

        # Store and compute signal line (EMA of MACD)
        self.macd_values.append(macd)
        if len(self.macd_values) < self.signal:
            return
        signal_line = ema(self.macd_values, self.signal)[-1]

        # Detect crossover
        if self.prev_macd is not None and self.prev_signal is not None:
            if self.prev_macd < self.prev_signal and macd > signal_line:
                # Bullish crossover: buy
                self.target = 1
            elif self.prev_macd > self.prev_signal and macd < signal_line:
                # Bearish crossover: sell
                self.target = -1
            else:
                self.target = 0
        else:
            self.target = 0

        # Update previous values for next tick
        self.prev_macd = macd
        self.prev_signal = signal_line
