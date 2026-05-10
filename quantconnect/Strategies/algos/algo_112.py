class Algo112(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("AAPL")
        self.AddEquity("GOOG")

    def update_targets(self):
        self.targets = {
            "SPY": 0.4,
            "AAPL": 0.3,
            "GOOG": 0.3
        }
