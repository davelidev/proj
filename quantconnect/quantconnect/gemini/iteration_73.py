from AlgorithmImports import *
import numpy as np

class GlobalSharpeRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL", "UGL", "TLT"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.MonthStart("TQQQ"), 
                         self.TimeRules.AfterMarketOpen("TQQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()), 64, Resolution.Daily)
        if hist.empty: return
        
        sharpe_scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                prices = hist.loc[symbol]['close'].values
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                if len(returns) < 60: continue
                
                mean_ret = returns.mean()
                std_ret = returns.std()
                sharpe = mean_ret / std_ret if std_ret > 0 else -100
                
                # Check for positive absolute momentum
                if (prices[-1] / prices[0]) - 1 > 0:
                    sharpe_scores[ticker] = sharpe
        
        if not sharpe_scores:
            self.Log(f"[{self.Time}] NO ASSETS WITH POSITIVE MOMENTUM. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        best_ticker = max(sharpe_scores, key=sharpe_scores.get)
        self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (Sharpe: {sharpe_scores[best_ticker]:.4f})")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
