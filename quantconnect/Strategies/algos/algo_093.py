class Algo093(BaseSubAlgo):
    """
    A simple equal-weight strategy that holds two ETFs.
    """
    def initialize(self):
        """Add securities to the algorithm."""
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        """Set target weights: equal allocation to both assets."""
        self.targets = {
            "SPY": 0.5,
            "QQQ": 0.5
        }
