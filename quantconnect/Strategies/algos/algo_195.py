class Algo195(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("TLT")
        self.AddEquity("GLD")
        self.prices = {"SPY": [], "TLT": [], "GLD": []}

    def update_targets(self):
        # Update price history
        for ticker in ["SPY", "TLT", "GLD"]:
            price = self.Securities[ticker].Close
            self.prices[ticker].append(price)

        # Ensure enough data for SPY (10-day and 30-day SMA)
        spy_prices = self.prices["SPY"]
        if len(spy_prices) < 30:
            self.targets = {"SPY": 1.0, "TLT": 0.0, "GLD": 0.0}
            return

        # Compute moving averages
        sma_10 = sum(spy_prices[-10:]) / 10.0
        sma_30 = sum(spy_prices[-30:]) / 30.0

        # Regime detection based on SMA crossover
        if sma_10 > sma_30:
            # Trending up – allocate fully to SPY
            self.targets = {"SPY": 1.0, "TLT": 0.0, "GLD": 0.0}
        else:
            # Mean-reverting – allocate to safe havens
            self.targets = {"SPY": 0.0, "TLT": 0.6, "GLD": 0.4}
