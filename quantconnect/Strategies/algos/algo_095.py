class Algo095(BaseSubAlgo):
    """
    Strategy: [Insert strategy description here]
    e.g., Simple equal-weight portfolio of selected equities.
    """

    def initialize(self):
        """
        Add initial securities to the algorithm.
        Override this method to define your universe.
        """
        # Example: Add three equity symbols
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """
        Update target weights for the current time step.
        Sets self.targets dict with symbol: weight (float).
        """
        # Example: Equal weight 1/3 each
        self.targets = {
            "SPY": 1.0 / 3,
            "QQQ": 1.0 / 3,
            "IWM": 1.0 / 3
        }
