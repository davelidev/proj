class Algo196(BaseSubAlgo):
    def initialize(self):
        # Add equity securities to track
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")
        # Add VIX as a proxy for market sentiment (note: VIX is an index, not an equity,
        # but we use AddEquity for simplicity in this structure)
        self.AddEquity("VIX")

    def update_targets(self):
        # Get current VIX price
        vix = self.Securities["VIX"].Price

        # Determine equity allocation based on VIX levels
        if vix > 30:
            # Reduce exposure (e.g., go to cash)
            equity_weight = 0.0
        elif vix < 15:
            # Increase exposure (fully invested)
            equity_weight = 1.0
        else:
            # Neutral zone – stay fully invested (or adjust as needed)
            equity_weight = 1.0

        # Set targets for the tracked equities (VIX itself is not traded in this strategy)
        self.targets = {
            "SPY": equity_weight,
            "QQQ": equity_weight,
            "IWM": equity_weight
        }
