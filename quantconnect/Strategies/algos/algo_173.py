class Algo173(BaseSubAlgo):
    """
    Strategy: Open-to-close range: wide open-close advantage.
    Looks for bars with an unusually wide open-close range, and
    takes a position in the direction of that range (long if
    close > open, short if close < open). Unusual is defined as
    more than a multiplier times the standard deviation above the
    rolling mean of absolute ranges.
    """

    def initialize(self):
        # Rolling window length
        self.window = 20
        # Number of standard deviations above the mean to trigger
        self.multiplier = 2.0
        # List to store recent absolute open-close ranges
        self.ranges = []

    def update_targets(self):
        """
        Called each bar. Expects self.data to have .open and .close
        attributes for the current bar. Sets self.target to:
          +1 for long,
          -1 for short,
           0 for flat.
        """
        # --- Retrieve current open and close ---
        try:
            o = self.data.open
            c = self.data.close
        except AttributeError:
            # If data structure is different, override in subclass
            return

        # Absolute range for the current bar
        current_range = abs(c - o)
        self.ranges.append(current_range)

        # Keep only the last `window` values
        if len(self.ranges) > self.window:
            self.ranges.pop(0)

        # Not enough data to calculate statistics – stay flat
        if len(self.ranges) < self.window:
            self.target = 0
            return

        # Rolling mean and sample standard deviation
        n = float(self.window)
        mean = sum(self.ranges) / n
        variance = sum((r - mean) ** 2 for r in self.ranges) / n
        std = variance ** 0.5

        # Threshold for “wide” range
        threshold = mean + self.multiplier * std

        # Decision logic
        if current_range > threshold:
            if c > o:
                self.target = 1   # wide bullish bar -> long
            else:
                self.target = -1  # wide bearish bar -> short
        else:
            self.target = 0       # no unusual range -> flat
