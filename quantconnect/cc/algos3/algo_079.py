class Algo079(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # Sector ETFs
        self.sectors = [
            "XLF", "XLE", "XLI", "XLV", "XLP",
            "XLY", "XLK", "XLU", "XLRE", "XLB", "XLC"
        ]
        
        self.symbols = [self.AddEquity(s, Resolution.Daily).Symbol for s in self.sectors]
        
        # 252-day low indicator for each symbol
        self.min252 = {sym: self.MIN(sym, 252, Resolution.Daily) for sym in self.symbols}
        
        # Warm up indicators
        self.SetWarmUp(252, Resolution.Daily)
        
        # Rebalance monthly on the first trading day
        self.Schedule.On(
            self.DateRules.MonthStart(self.symbols[0]),
            self.TimeRules.AfterMarketOpen(self.symbols[0], 0),
            self.Rebalance
        )
        
    def Rebalance(self):
        if self.IsWarmingUp:
            return
        
        eligible = []
        for sym in self.symbols:
            # Need current close and the 252-day low
            if not self.MIN(sym).IsReady:
                continue
            close = self.Securities[sym].Close
            low = self.MIN(sym).Current.Value
            if close > low:
                eligible.append(sym)
        
        if len(eligible) == 0:
            # No eligible sectors, go to cash
            self.Liquidate()
            return
        
        weight = 1.0 / len(eligible)
        for sym in eligible:
            self.SetHoldings(sym, weight)
        
        # Liquidate any sectors not in eligible
        for sym in self.symbols:
            if sym not in eligible and self.Portfolio[sym].Invested:
                self.SetHoldings(sym, 0)
