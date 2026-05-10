class Algo109(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
