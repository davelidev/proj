class Algo085(BaseSubAlgo):
    """
    A simple example algorithm that holds a portfolio of three ETFs in equal weights.
    """
    def initialize(self):
        # Add equity securities to the universe
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        # Set equal weights for each security
        symbols = ["SPY", "QQQ", "IWM"]
        weight = 1.0 / len(symbols)
        self.targets = {sym: weight for sym in symbols}
