class Algo097(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("TLT")
        self.AddEquity("IWM")
        self.AddEquity("GLD")

    def update_targets(self):
        self.targets = {
            "SPY": 0.25,
            "QQQ": 0.25,
            "TLT": 0.20,
            "IWM": 0.20,
            "GLD": 0.10
        }
