class Algo101(BaseSubAlgo):
    """
    Example strategy that adds three equities and sets equal target weights.
    """
    def initialize(self):
        """Add securities to the algorithm."""
        self.AddEquity("SPY")
        self.AddEquity("AAPL")
        self.AddEquity("MSFT")

    def update_targets(self):
        """Set portfolio target weights (must sum to 1.0 or less)."""
        self.targets = {
            "SPY": 0.4,
            "AAPL": 0.3,
            "MSFT": 0.3
        }
