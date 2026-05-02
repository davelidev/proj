from AlgorithmImports import *
import numpy as np

class SectorAlphaRotation(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2014, 1, 1)
        self.SetEndDate(2025, 12, 31)
        self.SetCash(100000)

        self.assets = ["TQQQ", "SOXL"]
        self.qqq = self.AddEquity("QQQ", Resolution.Daily).Symbol
        self.bil = self.AddEquity("BIL", Resolution.Daily).Symbol
        
        self.symbols = {}
        for ticker in self.assets:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol
            
        self.Schedule.On(self.DateRules.EveryDay("QQQ"), 
                         self.TimeRules.AfterMarketOpen("QQQ", 30), 
                         self.Rebalance)
                         
        self.SetWarmUp(64)

    def Rebalance(self):
        if self.Time.weekday() != 0: return # Mondays
        if self.IsWarmingUp: return
        
        hist = self.History(list(self.symbols.values()) + [self.qqq], 64, Resolution.Daily)
        if hist.empty: return
        
        try:
            q_prices = hist.loc[self.qqq]['close'].values
            q_ret = (q_prices[-1] / q_prices[0]) - 1
            
            alpha_scores = {}
            for ticker, symbol in self.symbols.items():
                if symbol in hist.index.get_level_values(0):
                    prices = hist.loc[symbol]['close'].values
                    asset_ret = (prices[-1] / prices[0]) - 1
                    # Alpha = Asset Return - Benchmark Return
                    alpha_scores[ticker] = asset_ret - q_ret
        except:
            return
            
        if not alpha_scores: return
        
        best_ticker = max(alpha_scores, key=alpha_scores.get)
        
        # Best must have positive alpha AND positive absolute momentum
        if alpha_scores[best_ticker] > 0 and q_ret > 0:
            self.Log(f"[{self.Time}] ROTATING TO {best_ticker} (Alpha: {alpha_scores[best_ticker]:.1%})")
            if not self.Portfolio[self.symbols[best_ticker]].Invested:
                self.SetHoldings(self.symbols[best_ticker], 1.0)
                for t, s in self.symbols.items():
                    if t != best_ticker: self.Liquidate(s)
                self.Liquidate(self.bil)
        else:
            self.Log(f"[{self.Time}] NO ALPHA OR NEGATIVE TREND. Moving to Cash.")
            self.Liquidate()
            self.SetHoldings(self.bil, 1.0)

    def OnData(self, data):
        pass
