class Algo128(BaseSubAlgo):
    """
    A simple algorithm that adds three equities with equal weighting.
    """

    def initialize(self):
        """Add securities to the universe."""
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """Set portfolio targets to equal weight."""
        self.targets = {
            "SPY": 1/3,
            "QQQ": 1/3,
            "IWM": 1/3
        }
