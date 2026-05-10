class Algo098(BaseSubAlgo):
    def initialize(self):
        self.AddEquity("SPY")
        self.AddEquity("QQQ")
        self.AddEquity("IWM")
        
    def update_targets(self):
        symbols = list(self.targets.keys()) if hasattr(self, 'targets') else ["SPY", "QQQ", "IWM"]
        # Ensure we have symbols from added securities; assume they are stored.
        # Alternatively, we could retrieve from self.Securities but need to avoid imports.
        # For simplicity, set equal weight for the predefined symbols.
        self.targets = {sym: 1.0/len(symbols) for sym in symbols}
