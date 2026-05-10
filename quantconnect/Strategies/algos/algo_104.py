class Algo104(BaseSubAlgo):
    """
    Strategy: Simple equal-weight allocation among added equities.
    """
    def initialize(self):
        """Add securities to the universe."""
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """Set target weights as an equal split among symbols."""
        symbols = list(self.targets.keys()) if hasattr(self, 'targets') else []
        if not symbols:
            # Assume we can get symbols from the algorithm's portfolio or securities
            # For simplicity, we'll use a fixed list (consistent with initialize)
            symbols = ["SPY", "QQQ", "IWM"]
        weight = 1.0 / len(symbols)
        self.targets = {sym: weight for sym in symbols}
