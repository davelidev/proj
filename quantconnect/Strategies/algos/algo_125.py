class Algo125(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
    
    def update_targets(self):
        self.targets = {"SPY": 1.0}
