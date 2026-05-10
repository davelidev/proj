class Algo129(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("BND")
    
    def update_targets(self):
        self.targets = {
            "SPY": 0.5,
            "BND": 0.5
        }
