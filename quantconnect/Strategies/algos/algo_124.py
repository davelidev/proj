class Algo124(BaseSubAlgo):
    # Strategy: Simple equal-weight allocation to two major ETFs
    def initialize(self):
        # Add securities to the algorithm
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        # Set portfolio targets as a dict {symbol: weight}
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
