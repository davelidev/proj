class Algo148(BaseSubAlgo):
    def initialize(self):
        # Parameters
        self.volume_period = 20          # number of updates for averaging
        self.imbalance_threshold = 0.6   # fraction of total volume to trigger signal
        
        # State
        self.volume_buffer = {}          # symbol -> list of latest net imbalances
        self.symbols = []                # populated by framework
        
    def update_targets(self):
        # Clear previous targets
        self.targets = {}
        
        # Process each symbol
        for sym in self.symbols:
            if sym not in self.data:
                continue
            
            # Extract recent trades (assumes self.data[sym] has list of (price, volume, direction))
            # direction: +1 for uptick, -1 for downtick, 0 for same
            trades = self.data[sym]
            
            # Calculate order imbalance: sum(volume * direction)
            net = sum(vol * dir for _, vol, dir in trades)
            total_volume = sum(vol for _, vol, _ in trades)
            
            # Maintain rolling window of net imbalances
            if sym not in self.volume_buffer:
                self.volume_buffer[sym] = []
            buf = self.volume_buffer[sym]
            buf.append(net)
            if len(buf) > self.volume_period:
                buf.pop(0)
            
            # Compute smoothed imbalance and its ratio to total volume
            smoothed_net = sum(buf) / len(buf)
            avg_total_volume = total_volume / len(trades) if trades else 1.0
            imbalance_ratio = smoothed_net / (avg_total_volume + 1e-9)
            
            # Generate signal
            if imbalance_ratio > self.imbalance_threshold:
                self.targets[sym] = 1.0   # long
            elif imbalance_ratio < -self.imbalance_threshold:
                self.targets[sym] = -1.0  # short
            else:
                self.targets[sym] = 0.0   # neutral
