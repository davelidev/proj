class Algo123(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("AAPL")
        self.AddEquity("MSFT")
        self.AddEquity("GOOGL")

    def update_targets(self):
        self.targets = {"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.3}
