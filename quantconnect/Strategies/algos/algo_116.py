class Algo116(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("TLT")

    def update_targets(self):
        self.targets = {"SPY": 0.5, "TLT": 0.5}
