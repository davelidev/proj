class Algo131(BaseSubAlgo):
    """
    Multi-MA consensus strategy:
    Long when price > SMA(20) > SMA(50) > SMA(200).
    """
    
    def initialize(self):
        self.sma_periods = [20, 50, 200]
        self.price_history = []  # expects external updates of close prices
        self.sma_values = {20: None, 50: None, 200: None}
        self.signal = 0  # 0 = flat, 1 = long
    
    def _compute_sma(self, period):
        """
        Calculate simple moving average over the most recent `period` prices.
        Returns None if insufficient data.
        """
        if len(self.price_history) < period:
            return None
        recent = self.price_history[-period:]
        return sum(recent) / period
    
    def update_targets(self):
        """Evaluate the current MA alignment and set the target signal."""
        for p in self.sma_periods:
            self.sma_values[p] = self._compute_sma(p)
        
        # Check if we have all required MAs
        if any(v is None for v in self.sma_values.values()):
            self.signal = 0
            return
        
        sma20 = self.sma_values[20]
        sma50 = self.sma_values[50]
        sma200 = self.sma_values[200]
        current_price = self.price_history[-1]
        
        # Long condition: price above all, and MAs in bullish alignment
        if current_price > sma20 > sma50 > sma200:
            self.signal = 1
        else:
            self.signal = 0
