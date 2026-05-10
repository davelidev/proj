class Algo130(BaseSubAlgo):
    def initialize(self):
        # Adding equities to the algorithm universe
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")
        self.AddEquity("TLT")

    def update_targets(self):
        # Set equal-weight allocation for all added securities
        equity_count = 4
        equal_weight = 1.0 / equity_count
        self.targets = {
            "SPY": equal_weight,
            "QQQ": equal_weight,
            "IWM": equal_weight,
            "TLT": equal_weight
        }
