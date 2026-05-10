class Algo138(BaseSubAlgo):
    """
    Momentum regime switch strategy:
    - MA(10) > MA(20) indicates uptrend mode.
    - In uptrend mode, target full investment (1.0).
    - Otherwise, target cash (0.0).
    """

    def __init__(self):
        super().__init__()
        # Moving average periods
        self.short_period = 10
        self.long_period = 20
        # Storage for price history (assumes self.data holds close prices)
        self.prices = []

    def initialize(self):
        """
        One-time setup. Reset price history and any state.
        """
        self.prices = []
        # Additional initialization (e.g., logging) can go here

    def update_targets(self):
        """
        Called each bar. Computes moving averages and sets portfolio targets.
        """
        # Assumes self.data contains the latest close price
        if not self.data:
            return  # No data yet

        latest_price = self.data[-1]
        self.prices.append(latest_price)

        # Only compute signals when enough prices are available
        if len(self.prices) < self.long_period:
            return

        # Calculate short MA (last 10 prices)
        short_ma = sum(self.prices[-self.short_period:]) / self.short_period

        # Calculate long MA (last 20 prices)
        long_ma = sum(self.prices[-self.long_period:]) / self.long_period

        # Determine regime
        uptrend = short_ma > long_ma

        # Set target allocation based on regime
        if uptrend:
            self.target_equity = 1.0  # fully invested
        else:
            self.target_equity = 0.0  # all cash

        # Additional target setting logic (e.g., for multiple assets) can be added here
