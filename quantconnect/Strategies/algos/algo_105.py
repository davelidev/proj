class Algo105(BaseSubAlgo):
    """
    Example algorithm that adds SPY equity and sets its target weight to 1.0.
    """
    def initialize(self):
        self.AddEquity("SPY")

    def update_targets(self):
        self.targets = {"SPY": 1.0}
