class Algo087(BaseSubAlgo):
    Strategy = "Long Equity"

    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        self.targets = {"SPY": 0.6, "QQQ": 0.4}
