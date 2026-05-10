class Algo106(BaseSubAlgo):
    """
    Strategy: Equal weight allocation among a set of equities.
    """
    def initialize(self):
        # Add securities to the algorithm's universe
        self.AddEquity("AAPL")
        self.AddEquity("MSFT")
        self.AddEquity("GOOGL")
        self.AddEquity("AMZN")
        self.AddEquity("TSLA")

    def update_targets(self):
        # Set equal weights for all symbols
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        weight = 1.0 / len(symbols)
        self.targets = {sym: weight for sym in symbols}
