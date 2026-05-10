class Algo083(BaseSubAlgo):
    def initialize(self):
        # Add securities to the algorithm
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
    
    def update_targets(self):
        # Set target weights for each symbol
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
