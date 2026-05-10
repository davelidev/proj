class Algo154(BaseSubAlgo):
    """
    Strategy: Money Flow (Chaikin Money Flow > 0) momentum signal.
    
    Methods:
        initialize(): Sets up indicator parameters.
        update_targets(data): Processes new bar data, computes CMF, 
                              and updates target (1=long, -1=short, 0=neutral).
    """
    
    def initialize(self):
        """Initialize the algorithm with default parameters."""
        self.cmf_period = 20                # Lookback period for CMF calculation
        self.bar_history = []               # Rolling list of bars (high, low, close, volume)
        self.cmf = 0.0                      # Current CMF value
        self.target = 0                     # Current trading target: 1=long, -1=short, 0=flat

    def update_targets(self, data):
        """
        Update trading targets based on CMF signal.
        
        Args:
            data: A bar object containing fields: high, low, close, volume.
        """
        # Extract current bar data
        high = data.high
        low = data.low
        close = data.close
        volume = data.volume

        # Store the bar in history
        self.bar_history.append((high, low, close, volume))
        
        # Keep only the last cmf_period bars
        if len(self.bar_history) > self.cmf_period:
            self.bar_history.pop(0)

        # Compute CMF only if we have enough bars
        if len(self.bar_history) == self.cmf_period:
            sum_money_flow_volume = 0.0
            sum_volume = 0.0
            for h, l, c, v in self.bar_history:
                # Money Flow Multiplier = ((Close - Low) - (High - Close)) / (High - Low)
                # Simplified: (2*Close - High - Low) / (High - Low)
                if h != l:
                    money_flow_multiplier = (2.0 * c - h - l) / (h - l)
                else:
                    money_flow_multiplier = 0.0   # Avoid division by zero
                
                money_flow_volume = money_flow_multiplier * v
                sum_money_flow_volume += money_flow_volume
                sum_volume += v

            # Calculate CMF
            self.cmf = sum_money_flow_volume / sum_volume if sum_volume != 0 else 0.0

            # Generate signal based on CMF sign
            if self.cmf > 0.0:
                self.target = 1    # Positive money flow → go long
            elif self.cmf < 0.0:
                self.target = -1   # Negative money flow → go short
            else:
                self.target = 0    # Neutral
        else:
            # Not enough data yet; stay flat
            self.target = 0
