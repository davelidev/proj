from AlgorithmImports import *

class BalancedAssetAllocation(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)
        
        # BAA-G12 Parameters
        # Canary Universe (Aggressive/Defensive Switch)
        self.canary = ["SPY", "IWM", "VEU", "BND"]
        
        # Offensive Universe (Top 12 Assets)
        self.offensive = [
            "SPY", "IWM", "VEU", "VWO", "VGK", "EWJ", 
            "EEM", "VNQ", "GLD", "DBC", "HYG", "LQD"
        ]
        
        # Defensive Universe
        # Use SHY instead of BIL if BIL has limited history or availability
        self.defensive = ["SHY", "IEF", "TLT"]
        
        self.symbols = list(set(self.canary + self.offensive + self.defensive))
        self.symbol_objs = {}
        for symbol in self.symbols:
            self.symbol_objs[symbol] = self.AddEquity(symbol, Resolution.Daily).Symbol

        # Rebalance monthly on the first trading day
        self.Schedule.On(self.DateRules.MonthStart("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(253, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        # 1. Calculate Momentum for Canary Universe
        canary_status = True
        for symbol in self.canary:
            score = self.GetMomentumScore(self.symbol_objs[symbol])
            if score <= 0:
                canary_status = False # Go Defensive if any canary asset has non-positive momentum
                break

        if canary_status:
            # 2. Offensive Mode: Pick Top 6 assets from Offensive Universe
            scores = {s: self.GetMomentumScore(self.symbol_objs[s]) for s in self.offensive}
            # Filter for positive momentum only
            positive_scores = {s: v for s, v in scores.items() if v > 0}
            if not positive_scores:
                # Fallback to defensive if no offensive assets have positive momentum
                self.GoDefensive()
                return
                
            sorted_offensive = sorted(positive_scores.items(), key=lambda x: x[1], reverse=True)[:6]
            
            # Liquidate non-target assets
            current_targets = [self.symbol_objs[s[0]] for s in sorted_offensive]
            for symbol in self.Portfolio.Keys:
                if symbol not in current_targets:
                    self.Liquidate(symbol)
                    
            # Set holdings equally
            weight = 1.0 / len(sorted_offensive)
            for s in sorted_offensive:
                self.SetHoldings(self.symbol_objs[s[0]], weight)
        else:
            self.GoDefensive()

    def GoDefensive(self):
        # 3. Defensive Mode: Pick the best Defensive asset
        defensive_scores = {s: self.GetMomentumScore(self.symbol_objs[s]) for s in self.defensive}
        best_defensive_ticker = max(defensive_scores, key=defensive_scores.get)
        best_defensive_symbol = self.symbol_objs[best_defensive_ticker]
        
        # Liquidate everything except best defensive
        for symbol in self.Portfolio.Keys:
            if symbol != best_defensive_symbol:
                self.Liquidate(symbol)
        
        self.SetHoldings(best_defensive_symbol, 1.0)

    def GetMomentumScore(self, symbol):
        history = self.History(symbol, 253, Resolution.Daily)
        if history.empty or len(history) < 252: return -100
        
        prices = history['close']
        
        p0 = prices.iloc[-1]
        p1 = prices.iloc[-22]  # ~1 month
        p3 = prices.iloc[-64]  # ~3 months
        p6 = prices.iloc[-127] # ~6 months
        p12 = prices.iloc[-253] # ~12 months
        
        return (12 * (p0/p1 - 1)) + (4 * (p0/p3 - 1)) + (2 * (p0/p6 - 1)) + (1 * (p0/p12 - 1))
