from AlgorithmImports import *
import numpy as np

class StableStrengthRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "QQQ"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(22)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                if len(returns) < 20: continue
                
                total_ret = (prices[-1] / prices[0]) - 1
                vol = np.std(returns)
                
                # Info Ratio = Return / Volatility
                scores[ticker] = total_ret / vol if vol > 0 else -100
        
        if not scores: return
        
        best_ticker = max(scores, key=scores.get)
        
        # Best must have positive momentum
        if scores[best_ticker] > 0:
            self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (IR: {scores[best_ticker]:.4f})")
            if not self.Portfolio[self.symbols[best_ticker]].Invested:
                self.SetHoldings(self.symbols[best_ticker], 1.0)
                for t in self.assets:
                    if t != best_ticker: self.Liquidate(self.symbols[t])
                self.Liquidate(self.bil)
        else:
            self.Log(f"[{self.Time}] NO STABLE POSITIVE TREND. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
