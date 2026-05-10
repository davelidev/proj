class Algo120(BaseSubAlgo):
    """
    Strategy: Equal-weight allocation between selected equities.
    """
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")

    def update_targets(self):
        self.targets = {"SPY": 0.5, "QQQ": 0.5}
