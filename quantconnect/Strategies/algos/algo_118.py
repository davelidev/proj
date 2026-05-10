class Algo118(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("TLT")

    def update_targets(self):
        self.targets = {"SPY": 0.5, "QQQ": 0.3, "TLT": 0.2}
