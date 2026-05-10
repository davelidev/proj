class Algo134(BaseSubAlgo):
    """
    Strategy: Drawdown cycles – track maximum drawdown and scale exposure accordingly.
    
    On each update (via `update_targets`), we compute the current drawdown from the peak 
    equity and scale the exposure linearly between 0 and 1 when drawdown exceeds a threshold.
    """
    
    def initialize(self):
        """Set initial state variables for drawdown tracking."""
        # Peak equity value (starting from 100 or whatever base is used)
        self.peak_equity = 100.0
        # Current maximum drawdown observed so far
        self.max_drawdown = 0.0
        # Current equity (should be updated externally via update_targets)
        self.current_equity = 100.0
        # Exposure scaling factor (0 to 1)
        self.exposure = 1.0
        # Drawdown threshold at which we begin reducing exposure (e.g., 10%)
        self.threshold = 0.10
        # Maximum drawdown beyond which exposure goes to zero (e.g., 25%)
        self.max_drawdown_limit = 0.25
        
    def update_targets(self):
        """
        Update exposure based on current drawdown from the peak equity.
        Expected that `self.current_equity` is set before calling this method.
        """
        # 1. Update peak equity
        if self.current_equity > self.peak_equity:
            self.peak_equity = self.current_equity
        
        # 2. Compute current drawdown as a fraction (0 to 1)
        if self.peak_equity > 0:
            self.current_drawdown = (self.peak_equity - self.current_equity) / self.peak_equity
        else:
            self.current_drawdown = 0.0
        
        # 3. Track the maximum drawdown ever observed
        if self.current_drawdown > self.max_drawdown:
            self.max_drawdown = self.current_drawdown
        
        # 4. Scale exposure linearly based on drawdown
        #    - At drawdown <= threshold: full exposure (1.0)
        #    - At drawdown >= max_drawdown_limit: zero exposure (0.0)
        #    - Between: linear interpolation
        if self.current_drawdown <= self.threshold:
            self.exposure = 1.0
        elif self.current_drawdown >= self.max_drawdown_limit:
            self.exposure = 0.0
        else:
            # linear mapping: (max_drawdown_limit - drawdown) / (max_drawdown_limit - threshold)
            self.exposure = (self.max_drawdown_limit - self.current_drawdown) / (self.max_drawdown_limit - self.threshold)
        
        # 5. (Optional) Add any target adjustment logic here, e.g., rebalancing weights
        #    The framework will use self.exposure to scale positions.
