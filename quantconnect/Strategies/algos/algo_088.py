class Algo088(BaseSubAlgo):
    """
    Strategy: Equal weight long positions in SPY and QQQ as a simple benchmark.
    """
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        # Maintain equal allocation to both equities
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
