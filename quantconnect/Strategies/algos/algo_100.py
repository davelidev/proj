class Algo100(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("TLT")

    def update_targets(self):
        self.targets = {"SPY": 0.4, "QQQ": 0.4, "TLT": 0.2}
