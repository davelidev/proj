class Algo091(BaseSubAlgo):
    """
    Sample algorithm that adds two equities and assigns equal weights.
    """
    def initialize(self):
        """Add securities to the algorithm."""
        self.AddEquity('AAPL')
        self.AddEquity('MSFT')

    def update_targets(self):
        """Set target weights for the securities."""
        self.targets = {'AAPL': 0.5, 'MSFT': 0.5}
