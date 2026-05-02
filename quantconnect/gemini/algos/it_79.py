from AlgorithmImports import *
import numpy as np

class KellyVolRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "UGL", "TLT"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.vol_target = 0.30 # 30% Annual Vol Target
        
        self.Schedule.On(self.DateRules.EveryDay("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(126) # 6 months to get better stats

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()), 64, Resolution.Daily)
        if hist.empty: return
        
        weights = {}
        total_kelly_weight = 0
        
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                if len(returns) < 60: continue
                
                mean_ret = returns.mean() * 252
                variance = returns.var() * 252
                
                # Kelly = Mean / Variance (Optimal fraction)
                # We use a conservative Half-Kelly
                kelly = 0.5 * (mean_ret / variance) if variance > 0 else 0
                kelly = max(0, kelly) # Long only
                
                weights[symbol] = kelly
                total_kelly_weight += kelly
        
        if total_kelly_weight == 0:
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Scale weights to meet Vol Target
        # Portfolio Vol (approx) = Sum(Weight * Asset Vol)
        # Simplified: We'll scale the Kelly weights so the highest one is capped,
        # then normalize to the vol target
        
        scaled_weights = {}
        for symbol, k in weights.items():
            # Apply Kelly and Vol scaling (Simplified parity)
            scaled_weights[symbol] = k / total_kelly_weight
            
        # Final execution
        for symbol, w in scaled_weights.items():
            self.SetHoldings(symbol, w)
            
        self.Liquidate(self.bil) # For residual cash

    def OnData(self, data):
        pass
