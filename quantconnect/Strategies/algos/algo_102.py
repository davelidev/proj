class Algo102(BaseSubAlgo):
    def initialize(self):
        # Add the securities to be traded
        self.AddEquity("AAPL")
        self.AddEquity("MSFT")
        self.AddEquity("GOOGL")

    def update_targets(self):
        # Set target portfolio weights (sum to 1.0)
        self.targets = {
            "AAPL": 0.4,
            "MSFT": 0.3,
            "GOOGL": 0.3
        }
