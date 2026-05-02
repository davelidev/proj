from AlgorithmImports import *
import numpy as np

class SharpeRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.tqqq = self.AddEquity("TQQQ", Resolution.Daily).Symbol
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.Schedule.On(self.DateRules.MonthStart("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.IsWarmingUp: return
        
        hist = self.History([self.tqqq, self.qqq], 64, Resolution.Daily)
        if hist.empty: return
        
        sharpe_scores = {}
        for symbol in [self.tqqq, self.qqq]:
            if symbol in hist.index.get_level_values(0):
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                if len(returns) < 60: continue
                
                mean_ret = returns.mean()
                std_ret = returns.std()
                # Simple Sharpe (ignoring risk-free rate for ranking)
                sharpe_scores[symbol] = mean_ret / std_ret if std_ret > 0 else -100
        
        if not sharpe_scores: return
        
        # Pick best performer by Sharpe
        best_symbol = max(sharpe_scores, key=sharpe_scores.get)
        
        # Safety: Best Sharpe must be positive
        if sharpe_scores[best_symbol] > 0:
            self.Log(f"[{self.Time}] ROTATING TO {best_symbol.Value} (Sharpe: {sharpe_scores[best_symbol]:.4f})")
            if not self.Portfolio[best_symbol].Invested:
                self.SetHoldings(best_symbol, 1.0)
                # Liquidate others
                for s in [self.tqqq, self.qqq]:
                    if s != best_symbol: self.Liquidate(s)
                self.Liquidate(self.bil)
        else:
            self.Log(f"[{self.Time}] NO POSITIVE SHARPE. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
