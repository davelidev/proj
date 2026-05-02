from AlgorithmImports import *
import numpy as np

class HighVolRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.sma = self.SMA(self.qqq, 200, Resolution.Daily)
        
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(200)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp or not self.sma.IsReady: return
        
        price_q = self.Securities[self.qqq].Price
        sma_val = self.sma.Current.Value
        
        if price_q < sma_val:
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)
            return
            
        # Bullish: Pick asset with highest 21-day volatility
        hist = self.History(list(self.symbols.values()), 22, Resolution.Daily)
        if hist.empty: return
        
        vol_scores = {}
        for ticker, symbol in self.symbols.items():
            if symbol in hist.index.get_level_values(0):
                returns = hist.loc[symbol]['close'].pct_change().dropna()
                vol_scores[ticker] = np.std(returns)
        
        if not vol_scores: return
        
        best_ticker = max(vol_scores, key=vol_scores.get)
        self.Log(f"[{self.Time}] BULL REGIME. Highest Vol: {best_ticker}.")
        
        if not self.Portfolio[self.symbols[best_ticker]].Invested:
            self.SetHoldings(self.symbols[best_ticker], 1.0)
            for t in self.assets:
                if t != best_ticker: self.Liquidate(self.symbols[t])
            self.Liquidate(self.bil)

    def OnData(self, data):
        pass
