class Algo103(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        # Equal weight allocation among the three equities
        self.targets = {"SPY": 1/3, "QQQ": 1/3, "IWM": 1/3}
