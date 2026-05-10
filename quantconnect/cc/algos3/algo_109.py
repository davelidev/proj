class Algo109(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014,1,1)
        self.SetEndDate(2025,12,31)
        self.SetCash(100000)
        self.AddEquity("TQQQ", Resolution.Daily)
        self.Securities["TQQQ"].SetDataNormalization(DataNormalizationMode.SplitAdjusted)
        self.range_window = RollingWindow[TradeBar](21)
        self.IsWarmingUp = True

    def OnData(self, data):
        if not data.ContainsKey("TQQQ"):
            return
        bar = data["TQQQ"]
        if bar is None:
            return
        
        # Warmup: first bar, just add and exit
        if self.IsWarmingUp:
            self.range_window.Add(bar)
            if self.range_window.IsReady:
                self.IsWarmingUp = False
            return
        
        self.range_window.Add(bar)
        if not self.range_window.IsReady:
            return
        
        # Extract range values from last 20 bars (excluding current)
        ranges = []
        for i in range(1, 21):
            prev_bar = self.range_window[i]
            ranges.append(prev_bar.High - prev_bar.Low)
        
        current_range = bar.High - bar.Low
        mean = sum(ranges) / len(ranges)
        variance = sum((r - mean) ** 2 for r in ranges) / len(ranges)
        std = variance ** 0.5
        
        lower_band = mean - 2 * std
        upper_band = mean + 2 * std
        
        # Volatility contraction -> anticipate expansion: buy
        if current_range < lower_band:
            self.SetHoldings("TQQQ", 1.0)
        # Volatility expansion -> exit
        elif current_range > upper_band:
            self.SetHoldings("TQQQ", 0)
        # else do nothing