class Algo160(BaseSubAlgo):
    """
    Reversal strategy based on consecutive losses.
    After two or more consecutive losing trades (or price movements),
    the algorithm reverses its current position.
    """

    def initialize(self):
        """
        Initialize state variables: track consecutive losses and last price.
        """
        self.consecutive_losses = 0        # count of consecutive losses
        self.previous_price = None         # last observed price for comparison
        # Assume BaseSubAlgo provides self.current_position (0, 1, or -1)
        # and self.symbol, self.prices, etc.

    def update_targets(self):
        """
        Update trading targets: check for reversal signal and adjust position.
        """
        # Obtain current price (assume BaseSubAlgo provides self.current_price()
        # or self.price_history). Simplified: use a placeholder.
        current_price = self.get_last_price()  # method provided by base class

        if self.previous_price is None:
            self.previous_price = current_price
            return

        # Determine if the latest price move was a loss relative to previous.
        # For a long position (1), a loss is when price goes down.
        # For a short position (-1), a loss is when price goes up.
        # If no position (0), we treat a down move as a loss (or define differently).
        if self.current_position == 1:          # long
            is_loss = current_price < self.previous_price
        elif self.current_position == -1:       # short
            is_loss = current_price > self.previous_price
        else:                                   # flat
            # For flat, we consider a down move as "loss" to trigger reversal long.
            # This is a design choice; adjust as needed.
            is_loss = current_price < self.previous_price

        if is_loss:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        # Reversal signal: 2 or more consecutive losses
        if self.consecutive_losses >= 2:
            # Reverse position: flip sign
            if self.current_position == 1:
                self.current_position = -1
            elif self.current_position == -1:
                self.current_position = 1
            else:
                # If flat, go long (or short, depending on preference)
                self.current_position = 1
            # Reset consecutive losses after reversal
            self.consecutive_losses = 0

        # Update previous price for next comparison
        self.previous_price = current_price

        # Optionally set target price based on new position (e.g., current price)
        # BaseSubAlgo might expect self.target_price to be set.
        self.target_price = current_price  # or compute a target

    # Helper method (may be provided by BaseSubAlgo)
    def get_last_price(self):
        """Return the most recent price (placeholder)."""
        # Assume BaseSubAlgo has a price feed.
        # In practice, this would be implemented by the base class.
        return self.prices[-1] if hasattr(self, 'prices') else 0.0
