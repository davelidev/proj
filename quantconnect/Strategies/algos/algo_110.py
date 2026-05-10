class Algo110(BaseSubAlgo):
    # Strategy: Simple equal-weight allocation between SPY and QQQ.
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
