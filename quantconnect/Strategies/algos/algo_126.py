class Algo126(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        # Example: equal weight allocation
        symbols = ["SPY", "QQQ", "IWM"]
        equal_weight = 1.0 / len(symbols)
        self.targets = {symbol: equal_weight for symbol in symbols}
