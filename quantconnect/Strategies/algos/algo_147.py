class Algo147(BaseSubAlgo):
    """
    Gamma scalping proxy: profit from volatility expansion.
    Implements a simplified gamma scalping strategy by dynamically adjusting
    delta exposure based on price deviations from a reference level,
    mimicking the convexity of a long option position.
    """
    def initialize(self):
        # Gamma target (notional exposure)
        self.gamma_target = 1000.0
        # Reference price (acts as option strike)
        self.strike_price = None
        # Keep track of last traded price for volatility proxy
        self.last_price = None
        # Growth factor to limit position size
        self.max_exposure = 0.2  # fraction of portfolio value

    def update_targets(self):
        # Retrieve current price and portfolio value (assumed available from BaseSubAlgo)
        current_price = getattr(self, 'price', None)
        portfolio_value = getattr(self, 'portfolio_value', None)
        symbol = getattr(self, 'symbol', None)

        if current_price is None or portfolio_value is None or symbol is None:
            return

        # Initialize strike price on first call
        if self.strike_price is None:
            self.strike_price = current_price

        # Price move from strike (proxy for option moneyness)
        price_deviation = current_price - self.strike_price

        # Gamma scalping: delta ≈ gamma * (S - K)
        # This gives a convex payoff: buy when price rises, sell when falls
        target_delta = self.gamma_target * price_deviation

        # Convert delta to number of shares (assuming each share has delta 1)
        target_shares = target_delta

        # Apply portfolio constraints
        max_shares = int(portfolio_value * self.max_exposure / current_price)
        target_shares = max(-max_shares, min(max_shares, int(target_shares)))

        # Update position (method may vary by framework; assume set_target exists)
        if hasattr(self, 'set_target'):
            self.set_target(symbol, target_shares)

        # Optionally update strike price to reflect new market level
        # (In real scalping, strike is fixed; here we keep it as entry price)
        # To capture volatility expansion, we can leave strike unchanged
        # Or reset periodically: if abs(price_deviation) > threshold, reset strike
        # For simplicity, we keep the original strike.

        # Update last price for any additional logic
        self.last_price = current_price
