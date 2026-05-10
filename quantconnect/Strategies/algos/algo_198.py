class Algo198(BaseSubAlgo):
    """
    Strategy: Reduce exposure when HY OAS > 500 bps.
    """
    def initialize(self):
        # Add securities to the universe
        self.AddEquity("SPY")      # S&P 500 ETF
        self.AddEquity("HYG")      # High Yield Corporate Bond ETF
        self.AddEquity("TLT")      # Long‑Term Treasury ETF

    def update_targets(self):
        # Retrieve current HY OAS value (assumed to be set by external data feed)
        hy_oas = getattr(self, 'hy_oas', 0)

        if hy_oas > 500:
            # Credit spreads are too wide → reduce exposure
            self.targets = {"SPY": 0.0, "HYG": 0.0, "TLT": 0.0}
        else:
            # Normal conditions: maintain desired targets
            self.targets = {"SPY": 0.5, "HYG": 0.2, "TLT": 0.3}
