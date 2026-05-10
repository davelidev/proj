class Algo193(BaseSubAlgo):
    """
    Volatility clustering strategy: vol begets vol.
    Uses recent volatility to adjust target weights inversely proportional to volatility.
    """
    def initialize(self):
        # Add securities
        self.symbols = ["SPY", "IWM", "QQQ"]
        for sym in self.symbols:
            self.AddEquity(sym)

        # Store recent closes and returns for volatility computation
        self.price_hist = {sym: [] for sym in self.symbols}
        self.return_hist = {sym: [] for sym in self.symbols}
        self.lookback = 20  # Number of periods for volatility estimation

    def update_targets(self):
        # Update price history and compute returns
        current_prices = {}
        for sym in self.symbols:
            try:
                close = self.Securities[sym].Close
            except AttributeError:
                close = None
            if close is not None:
                self.price_hist[sym].append(close)
                if len(self.price_hist[sym]) > self.lookback + 1:
                    self.price_hist[sym].pop(0)
                if len(self.price_hist[sym]) >= 2:
                    returns = (self.price_hist[sym][-1] - self.price_hist[sym][-2]) / self.price_hist[sym][-2]
                    self.return_hist[sym].append(returns)
                    if len(self.return_hist[sym]) > self.lookback:
                        self.return_hist[sym].pop(0)

        # Compute volatilities (standard deviation of returns)
        vols = {}
        for sym in self.symbols:
            hist = self.return_hist[sym]
            if len(hist) < self.lookback:
                vols[sym] = float('inf')  # Unavailable -> skip
            else:
                mean_ret = sum(hist) / len(hist)
                variance = sum((r - mean_ret) ** 2 for r in hist) / len(hist)
                vols[sym] = variance ** 0.5

        # Set targets: inverse vol weighting (ignoring missing volatilities)
        total_inv_vol = 0.0
        for sym in self.symbols:
            if vols[sym] > 0 and vols[sym] != float('inf'):
                total_inv_vol += 1.0 / vols[sym]
        if total_inv_vol > 0:
            targets = {}
            for sym in self.symbols:
                if vols[sym] > 0 and vols[sym] != float('inf'):
                    targets[sym] = (1.0 / vols[sym]) / total_inv_vol
                else:
                    targets[sym] = 0.0
            self.targets = targets
        else:
            self.targets = {sym: 0.0 for sym in self.symbols}
