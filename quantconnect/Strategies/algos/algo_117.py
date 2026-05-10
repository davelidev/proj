class Algo117(BaseSubAlgo):
    Strategy = "EqualWeightSPY"

    def initialize(self):
        self.AddEquity("SPY")

    def update_targets(self):
        self.targets = {"SPY": 1.0}
