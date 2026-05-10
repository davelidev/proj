class Algo089(BaseSubAlgo):
    """
    Strategy: Simple equal-weight allocation among four ETFs: SPY, QQQ, TLT, GLD.
    """
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("TLT")
        self.AddEquity("GLD")

    def update_targets(self):
        self.targets = {
            "SPY": 0.25,
            "QQQ": 0.25,
            "TLT": 0.25,
            "GLD": 0.25
        }
