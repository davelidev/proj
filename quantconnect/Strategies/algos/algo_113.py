class Algo113(BaseSubAlgo):
    """
    A minimal algorithmic trading strategy that holds equal weights across three equity ETFs.
    Implements the required methods: initialize() and update_targets().
    """

    def initialize(self):
        """
        Initialize the algorithm by adding the desired securities to the data universe.
        """
        # Add three major equity ETFs
        self.AddEquity("SPY")   # S&P 500 ETF
        self.AddEquity("QQQ")   # Nasdaq-100 ETF
        self.AddEquity("IWM")   # Russell 2000 ETF

    def update_targets(self):
        """
        Update target portfolio weights (self.targets) each bar.
        This implementation uses an equal-weight allocation among all added securities.
        """
        # Retrieve the list of symbols that have been added via AddEquity
        # (In a real framework, you might store them; here we assume we know them.)
        symbols = ["SPY", "QQQ", "IWM"]
        # Compute equal weight per symbol
        weight = 1.0 / len(symbols)
        # Build the targets dictionary
        self.targets = {symbol: weight for symbol in symbols}
