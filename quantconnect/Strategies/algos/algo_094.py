class Algo094(BaseSubAlgo):
    def initialize(self):
        # Add equity securities (e.g., SPY and QQQ as a simple example)
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        # Additional securities could be added here if desired

    def update_targets(self):
        # Set equal-weight targets for the added securities
        self.targets = {
            "SPY": 0.5,
            "QQQ": 0.5
        }
