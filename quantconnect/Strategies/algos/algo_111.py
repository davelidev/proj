class Algo111(BaseSubAlgo):
    """
    Strategy: A simple equity-based algorithm that adds securities during initialization
    and sets target weights for the portfolio during each rebalance.
    """
    def initialize(self):
        """
        Called once at the start of the algorithm.
        Adds securities to the universe.
        """
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")

    def update_targets(self):
        """
        Called each time the algorithm needs to rebalance.
        Sets the target weights for each symbol in the portfolio.
        """
        self.targets = {
            "SPY": 0.5,
            "QQQ": 0.3,
            "IWM": 0.2
        }
