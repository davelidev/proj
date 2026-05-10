class Algo157(BaseSubAlgo):
    """
    Resistance probe strategy:
    - Identify a resistance level (e.g., recent high).
    - Detect when price tests that level (touches within a small tolerance).
    - If price closes above resistance and holds for a defined number of bars,
      generate a long target at the current price.
    """

    def initialize(self):
        """Initialize strategy parameters and compute initial resistance."""
        # Number of bars price must hold above resistance before generating target
        self.hold_required = 3

        # Count of consecutive bars above resistance
        self.hold_count = 0

        # Whether price has recently tested the resistance level
        self.tested = False

        # Tolerance for testing resistance (0.5% above/below)
        self.test_tolerance = 0.005

        # Resistance level (will be computed from first batch of data)
        self.resistance = None

        # Compute initial resistance from first 20 bars if data is available
        if hasattr(self, 'data') and self.data and len(self.data) >= 20:
            initial_prices = [self.data[i] for i in range(20)]
            self.resistance = max(initial_prices)

        # Initialize targets list if not already present
        if not hasattr(self, 'targets'):
            self.targets = []

        # Internal bar counter (optional, for dynamic resistance updates)
        self.bar_count = 0

    def update_targets(self):
        """Called on each new bar. Check price action relative to resistance."""
        # Ensure data exists
        if not hasattr(self, 'data') or not self.data:
            return

        current_price = self.data[-1]
        self.bar_count += 1

        # Dynamically recompute resistance every 20 bars if not set yet
        if self.resistance is None and len(self.data) >= 20:
            self.resistance = max(self.data[-20:])

        if self.resistance is None:
            # No resistance computed yet – skip logic
            return

        # --- Step 1: Check if price is testing resistance ---
        # Test condition: price within test_tolerance of resistance
        lower_bound = self.resistance * (1 - self.test_tolerance)
        upper_bound = self.resistance * (1 + self.test_tolerance)
        if lower_bound <= current_price <= upper_bound:
            self.tested = True

        # --- Step 2: Check for breakout confirmation ---
        # If price is clearly above resistance (more than tolerance)
        if current_price > self.resistance * (1 + self.test_tolerance):
            self.hold_count += 1
            # Retain 'tested' flag once set (do not reset here)
        else:
            # Price fell back below or at resistance
            self.hold_count = 0
            self.tested = False  # Reset test flag if price retreats

        # --- Step 3: Generate target if conditions met ---
        if self.tested and self.hold_count >= self.hold_required:
            # Add a long target at the current price
            if not hasattr(self, 'targets'):
                self.targets = []
            self.targets.append(current_price)

            # Reset counters to avoid duplicate triggers
            self.hold_count = 0
            self.tested = False

        # Optional: Adjust resistance if price moves far above (new resistance level)
        # For simplicity, keep static; could be updated by a higher level in production.
