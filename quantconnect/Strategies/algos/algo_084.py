class Algo084(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        self.targets = {
            "SPY": 1.0 / 3,
            "QQQ": 1.0 / 3,
            "IWM": 1.0 / 3
        }
