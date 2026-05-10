class Algo127(BaseSubAlgo):
    def initialize(self):
        """Add securities to the algorithm."""
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """Set target weights for all securities equally."""
        self.targets = {
            "SPY": 1.0 / 3,
            "QQQ": 1.0 / 3,
            "IWM": 1.0 / 3
        }
