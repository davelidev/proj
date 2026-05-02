from AlgorithmImports import *
import numpy as np

class SmartBetaRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "QQQ"]
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.EveryDay("SPY"), 
                         self.TimeRules.AfterMarketOpen("SPY", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()) + [self.spy], 64, Resolution.Daily)
        if hist.empty: return
        
        try:
            spy_ret = hist.loc[self.spy]['close'].pct_change().dropna()
            scores = {}
            for ticker, symbol in self.symbols.items():
                if symbol in hist.index.get_level_values(0):
                    asset_ret = hist.loc[symbol]['close'].pct_change().dropna()
                    if len(asset_ret) < 60: continue
                    
                    # Calculate Beta
                    covariance = np.cov(asset_ret, spy_ret)[0][1]
                    variance = np.var(spy_ret)
                    beta = covariance / variance if variance > 0 else 1.0
                    
                    total_ret = (hist.loc[symbol]['close'][-1] / hist.loc[symbol]['close'][0]) - 1
                    
                    # Rank by Return / Beta (avoiding zero division)
                    scores[ticker] = total_ret / max(0.1, abs(beta))
        except:
            return
            
        if not scores: return
        
        best_ticker = max(scores, key=scores.get)
        
        # Best must have positive momentum
        if scores[best_ticker] > 0:
            self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (Ret/Beta: {scores[best_ticker]:.4f})")
            if not self.Portfolio[self.symbols[best_ticker]].Invested:
                self.SetHoldings(self.symbols[best_ticker], 1.0)
                for t, s in self.symbols.items():
                    if t != best_ticker: self.Liquidate(s)
                self.Liquidate(self.bil)
        else:
            self.Log(f"[{self.Time}] NO ASSETS WITH POSITIVE BETA-ALPHA. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
