class Algo107(BaseSubAlgo):
    """
    Strategy: A simple equity allocation strategy.
    """
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        self.targets = {
            "SPY": 0.5,
            "QQQ": 0.3,
            "IWM": 0.2
        }
