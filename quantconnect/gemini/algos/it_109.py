from AlgorithmImports import *

class DefensiveAssetAllocation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        # Canary Assets (Protective Universe)
        self.canary = ["VWO", "BND"]
        
        # Offensive Assets (Risky Universe)
        self.offensive = ["SPY", "IWM", "VEU", "VNQ"]
        
        # Defensive Assets (Safe Universe)
        self.defensive = ["SHY", "IEF", "LQD"]
        
        self.all_symbols = self.canary + self.offensive + self.defensive
        self.symbol_objs = {}
        
        for symbol in self.all_symbols:
            self.symbol_objs[symbol] = self.AddEquity(symbol, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.MonthStart("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(252, Resolution.Daily)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        # Calculate Momentum Score for Canary Assets
        # Score = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)
        
        canary_scores = {}
        for ticker in self.canary:
            symbol = self.symbol_objs[ticker]
            history = self.History(symbol, 253, Resolution.Daily)
            if history.empty or len(history) < 252: continue
            
            price = history['close']
            r1 = (price.iloc[-1] / price.iloc[-22]) - 1
            r3 = (price.iloc[-1] / price.iloc[-64]) - 1
            r6 = (price.iloc[-1] / price.iloc[-127]) - 1
            r12 = (price.iloc[-1] / price.iloc[-253]) - 1
            
            canary_scores[symbol] = (12 * r1) + (4 * r3) + (2 * r6) + (1 * r12)

        if not canary_scores: return

        # Determine Regime
        # If any canary asset has a negative score, move to defensive
        if any(score < 0 for score in canary_scores.values()):
            # Defensive Regime: Pick the best defensive asset
            defensive_scores = {}
            for ticker in self.defensive:
                symbol = self.symbol_objs[ticker]
                history = self.History(symbol, 253, Resolution.Daily)
                if history.empty: continue
                price = history['close']
                defensive_scores[symbol] = (price.iloc[-1] / price.iloc[-253]) - 1
            
            best_defensive = max(defensive_scores, key=defensive_scores.get)
            
            # Liquidate others
            for ticker in self.offensive:
                self.Liquidate(self.symbol_objs[ticker])
            for ticker in self.defensive:
                if self.symbol_objs[ticker] != best_defensive:
                    self.Liquidate(self.symbol_objs[ticker])
                    
            self.SetHoldings(best_defensive, 1.0)
        else:
            # Offensive Regime: Pick the best offensive asset
            offensive_scores = {}
            for ticker in self.offensive:
                symbol = self.symbol_objs[ticker]
                history = self.History(symbol, 253, Resolution.Daily)
                if history.empty: continue
                price = history['close']
                offensive_scores[symbol] = (price.iloc[-1] / price.iloc[-253]) - 1
            
            best_offensive = max(offensive_scores, key=offensive_scores.get)
            
            # Liquidate others
            for ticker in self.defensive:
                self.Liquidate(self.symbol_objs[ticker])
            for ticker in self.offensive:
                if self.symbol_objs[ticker] != best_offensive:
                    self.Liquidate(self.symbol_objs[ticker])
                    
            self.SetHoldings(best_offensive, 1.0)

    def OnData(self, data):
        pass
