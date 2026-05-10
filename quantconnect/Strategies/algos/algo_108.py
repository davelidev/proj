class Algo108(BaseSubAlgo):
    def initialize(self):
        # Add equities to the algorithm
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        # Set equal weight targets for the three equities
        self.targets = {
            "SPY": 1.0 / 3,
            "QQQ": 1.0 / 3,
            "IWM": 1.0 / 3
        }
