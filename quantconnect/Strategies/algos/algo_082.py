class Algo082(BaseSubAlgo):
    """
    Strategy: Simple equal-weight allocation to a basket of equities.
    """
    def initialize(self):
        """Add securities to the algorithm."""
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """Set target weights for each symbol."""
        # Equal weight allocation
        self.targets = {
            "SPY": 1/3,
            "QQQ": 1/3,
            "IWM": 1/3
        }
