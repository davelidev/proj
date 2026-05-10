class Algo149(BaseSubAlgo):
    """
    Micro-structure strategy: bid-ask bounce fading.
    Detects price bounces between bid and ask and fades the move.
    """

    def initialize(self):
        """
        Initialize strategy parameters and data structures.
        """
        # Parameters
        self.lookback = 5          # number of recent quotes to analyze
        self.bounce_threshold = 0.01  # minimum price move to qualify as bounce
        self.target_pct = 0.1      # fraction of portfolio value per position

        # Storage for recent quotes per symbol (list of (bid, ask))
        self.quotes_history = {sym: [] for sym in self.symbols}

    def update_targets(self):
        """
        Update target positions based on bid-ask bounce detection.
        """
        for symbol in self.symbols:
            # Get current quote (assumed bid/ask available)
            quote = self.get_quote(symbol)  # method expected from BaseSubAlgo
            if quote is None:
                continue
            bid, ask = quote['bid'], quote['ask']
            if bid is None or ask is None or bid >= ask:
                continue

            # Update history
            history = self.quotes_history[symbol]
            history.append((bid, ask))
            if len(history) > self.lookback + 1:
                history.pop(0)

            # Need at least lookback+1 entries to detect bounce
            if len(history) < self.lookback + 1:
                self.set_target(symbol, 0)  # no signal yet
                continue

            # Analyze last two quotes: check for bounce from bid to ask or ask to bid
            recent = history[-2:]   # last two pairs of (bid, ask)
            prev_bid, prev_ask = recent[0]
            curr_bid, curr_ask = recent[1]

            # Check if price jumped from bid to ask (down to up bounce)
            if prev_ask <= prev_bid + self.bounce_threshold and prev_bid == prev_ask:
                # In a steady state, maybe not a bounce
                pass

            # Detect bounce: last tick moved from near the bid to near the ask (or vice versa)
            # Simple heuristic: compare mid prices
            prev_mid = (prev_bid + prev_ask) / 2.0
            curr_mid = (curr_bid + curr_ask) / 2.0
            mid_change = curr_mid - prev_mid

            if abs(mid_change) < self.bounce_threshold:
                # No significant movement, fade nothing
                self.set_target(symbol, 0)
                continue

            # Determine if it was a bounce from bid side (upward) or ask side (downward)
            # Upward bounce: previous price near bid, current price near ask
            if abs(prev_mid - prev_bid) < self.bounce_threshold and abs(curr_mid - curr_ask) < self.bounce_threshold:
                # Bounce up from bid: fade by shorting
                target_shares = -int(self.portfolio_value * self.target_pct / curr_ask)
                self.set_target(symbol, target_shares)
            elif abs(prev_mid - prev_ask) < self.bounce_threshold and abs(curr_mid - curr_bid) < self.bounce_threshold:
                # Bounce down from ask: fade by buying
                target_shares = int(self.portfolio_value * self.target_pct / curr_bid)
                self.set_target(symbol, target_shares)
            else:
                self.set_target(symbol, 0)

    # ------------------------------------------------------------------
    # Helper methods expected from BaseSubAlgo (not defined here)
    # ------------------------------------------------------------------
    def get_quote(self, symbol):
        """Placeholder: returns dict with 'bid' and 'ask'."""
        raise NotImplementedError

    def set_target(self, symbol, shares):
        """Placeholder: sets target quantity for symbol."""
        raise NotImplementedError

    @property
    def portfolio_value(self):
        """Placeholder: total portfolio value."""
        raise NotImplementedError
