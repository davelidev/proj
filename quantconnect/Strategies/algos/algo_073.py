class Algo073(BaseSubAlgo):
    def initialize(self):
        # Call base initialization (sets dates, cash)
        super().Initialize()

        # Add sector ETFs and VIX index
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.xlu = self.AddEquity("XLU", Resolution.Daily).Symbol
        self.xlp = self.AddEquity("XLP", Resolution.Daily).Symbol
        self.vix = self.AddIndex("VIX", Resolution.Daily).Symbol

        # Set benchmark (optional)
        self.SetBenchmark(self.spy)

    def update_targets(self):
        # Wait until we have at least one VIX price data point
        if not self.CurrentSlice.ContainsKey(self.vix):
            return

        vix_value = self.CurrentSlice[self.vix].Close

        # Defensive switch: if VIX > 25, hold utilities and staples equally
        if vix_value > 25:
            self.targets = {
                self.xlu: 0.50,
                self.xlp: 0.50
            }
        else:
            # Normal environment: hold broad market (SPY)
            self.targets = {
                self.spy: 1.00
            }
