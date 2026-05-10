class Algo092(BaseSubAlgo):
    def initialize(self):
        # Add securities to the algorithm
        self.AddEquity("AAPL")
        self.AddEquity("MSFT")
        self.AddEquity("GOOGL")

    def update_targets(self):
        # Simple equal weight strategy
        self.targets = {
            "AAPL": 1/3,
            "MSFT": 1/3,
            "GOOGL": 1/3
        }
